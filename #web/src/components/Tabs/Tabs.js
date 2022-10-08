import './Tabs.css';
import {Component} from "react";

const domId = (id) => document.getElementById(id);

function DefaultNewTabPage({uid}) {
    return (
        <section style={{padding: "10px"}}>
            <h1>New Tab Section {uid}</h1>
            <input/>
        </section>
    );
}

function Tab({children, className, ...props}) {
    return (
        <span className={"Tab " + (className ? className : "")} {...props}>
            {children}
        </span>
    );
}

let guid = 0;

export default class Tabs extends Component {
    prefix = "TabsUIdPrefix--some-string-to-make-this-difficult-to-clash-with-user-defined-id";
    tabMinWidth = 70;
    tabMaxWidth = 130;
    sanityOffset = 33;
    static defaultProps = {
        newTabPage: DefaultNewTabPage,
        tabPages: [],
        activeTab: 0,
    };

    constructor(props) {
        super(props);
        this.uid = 0;
        this.vis = this.props.tabPages.length;
        this.scrollTab = this.vis - 1;
        this.state = {tabPages: props.tabPages, activeTab: props.activeTab, resize: null};
        this.prefix += guid++;
    }

    componentDidMount() {
        if (this.state.tabPages.length === 0) this.onNewTabClick();
        window.addEventListener('resize', () => this.setState({resize: null}));
        this.setState({resize: true});
    }

    onTabClick = (i) => {
        this.setState({activeTab: i});
    }

    onNewTabClick = () => {
        const tabPages = [...this.state.tabPages, <this.props.newTabPage uid={this.uid++}/>];
        this.scrollTab = this.state.tabPages.length;
        this.setState({tabPages: tabPages, activeTab: this.state.tabPages.length});
    }

    onXClick = (i) => {
        const tabPages = [...this.state.tabPages.slice(0, i), ...this.state.tabPages.slice(i + 1)];
        const activeTab = i === this.state.activeTab ?
            (i === tabPages.length ? i - 1 : i) :
            (i > this.state.activeTab ? this.state.activeTab : this.state.activeTab - 1);
        this.scrollTab = Math.min(
            Math.max(activeTab + (this.scrollTab - this.state.activeTab), this.vis - 1),
            tabPages.length - 1
        );
        this.setState({tabPages: tabPages, activeTab: activeTab});
    }

    getTabs = (tabMinWidth) => (
        this.state.tabPages.map(page => {
            const i = this.state.tabPages.indexOf(page);
            return (
                <Tab key={Math.random()}
                     id={this.prefix + "Tab" + i}
                     onClick={() => this.onTabClick(i)}
                     visible={i <= this.scrollTab && i > this.scrollTab - this.vis ? 1 : 0}
                     active={i === this.state.activeTab ? 1 : 0}
                     style={{
                         minWidth: tabMinWidth ? tabMinWidth : this.tabMinWidth,
                         maxWidth: this.tabMaxWidth,
                     }}>
                    <span>Tab:{i}</span>
                    <code visible={this.state.tabPages.length !== 1 ? 1 : 0} onClick={(e) => {
                        this.onXClick(i);
                        e.stopPropagation();
                    }}>X</code>
                </Tab>
            );
        })
    )

    tabScroll = (dir) => {
        let TabA, TabB, inc;
        if (dir > 0) {
            inc = 1;
            TabA = domId(this.prefix + "Tab" + (this.scrollTab - this.vis + 1));
            TabB = domId(this.prefix + "Tab" + (this.scrollTab + 1));
        } else {
            inc = -1;
            TabA = domId(this.prefix + "Tab" + (this.scrollTab));
            TabB = domId(this.prefix + "Tab" + (this.scrollTab - this.vis));
        }
        if (TabA && TabB) {
            dir !== 0 && TabA.setAttribute("visible", "0");
            TabB.setAttribute("visible", "1");
            this.scrollTab += inc;
            domId(this.prefix + "tool<").setAttribute("disable",
                this.scrollTab === this.vis - 1 ? "1" : "0");
            domId(this.prefix + "tool>").setAttribute("disable",
                this.scrollTab + 1 === this.state.tabPages.length ? "1" : "0");
        }
    }

    responsiveTabs = () => {
        let Tabs = domId(this.prefix + "Tabs"), Tools = domId(this.prefix + "Tools");
        let cntTabs = domId(this.prefix + "container--tabs");
        let tabsWidth, tabMinWidth, tabsWidthRem;
        if (Tabs) {
            let full = cntTabs.offsetWidth - Tools.offsetWidth - this.sanityOffset;
            tabMinWidth =
                Math.min(Math.max(full / this.state.tabPages.length, this.tabMinWidth), this.tabMaxWidth);
            tabsWidth =
                Math.min(tabMinWidth * (this.vis = Math.max(full / tabMinWidth | 0, 1)), tabMinWidth * this.state.tabPages.length);
            tabsWidthRem = full - tabsWidth;
            this.vis = Math.min(this.vis, this.state.tabPages.length)
            if (this.vis < this.state.tabPages.length) {
                tabMinWidth += tabsWidthRem / this.vis;
                tabsWidth = full;
                tabsWidthRem = 0;
            }
            domId(this.prefix + "tool<").setAttribute("disable",
                this.scrollTab === this.vis - 1 ? "1" : "0");
            domId(this.prefix + "tool>").setAttribute("disable",
                this.scrollTab + 1 === this.state.tabPages.length ? "1" : "0");
        }
        return {tabsWidth, tabMinWidth, tabsWidthRem};
    }

    render() {
        const {tabsWidth, tabMinWidth, tabsWidthRem} = this.responsiveTabs();
        const tabs = this.getTabs(tabMinWidth);
        return (
            <div className="container">
                <div id={this.prefix + "container--tabs"} className="container--tabs">
                    <span style={{minWidth: this.sanityOffset}}/>
                    <div id={this.prefix + "Tabs"} className="Tabs" style={{maxWidth: tabsWidth}}>{tabs}</div>
                    <div id={this.prefix + "Tools"} className="Tools">
                        <button className="tool" onClick={this.onNewTabClick}>+</button>
                        <button disable={this.scrollTab === this.vis - 1 ? 1 : 0} className="tool"
                                id={this.prefix + "tool<"} onClick={() => this.tabScroll(-1)}>{"<"}</button>
                        <button disable={this.scrollTab + 1 === this.state.tabPages.length ? 1 : 0}
                                className="tool"
                                id={this.prefix + "tool>"} onClick={() => this.tabScroll(+1)}>{">"}</button>
                    </div>
                </div>
                <div className="container--page">
                    <div className={"page-buffer"}/>
                    {this.state.tabPages.map((page) =>
                        <div key={page.props.uid}
                             style={{
                                 display:
                                     this.state.tabPages.indexOf(page) !== this.state.activeTab ? 'none' : 'initial'
                             }}>
                            {page}
                        </div>)}
                </div>
            </div>
        )
    }
}
