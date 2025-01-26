
function Navigation() {
    return (
      <nav className="navigation">
        <img
        src = "/Logo.svg"
        alt = "Little Lemon restaurant logo"
        />
        <ul className="nav-menu">
            <li className="menu-item"><a href = "./HomePage">Home</a></li>
            <li className="menu-item"><a href = "./About">About</a></li>
            <li className="menu-item"><a href = "./Menu">Menu</a></li>
            <li className="menu-item"><a href = "./BookingPage">Reservations</a></li>
            <li className="menu-item"><a href = "./OrderOnline">Order Online</a></li>
            <li className="menu-item"><a href = "./Login">Login</a></li>
        </ul>
      </nav>
    );
  }

  export default Navigation;
