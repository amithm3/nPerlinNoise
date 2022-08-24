import logo from './logo.svg'
import './Nav&Foo.css'

function Nav() {
    return (
        <div className="Nav">
            <img src={logo} alt="logo" id="nav--logo"/>
        </div>
    )
}

function Foo() {
    return (
        <div className="Foo">
            <h1>Footer</h1>
        </div>
    )
}

export {Nav, Foo}
