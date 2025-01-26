import restauranfood from './restauranfood.jpg';

function Header() { 
    return (
        <div className="header-container">
        <div className="header-text">
            <br /><h1>Little Lemon</h1><br />
            
            <h3>Chicago</h3>
            <h6><i>A small family-owned restaurant, that offers different Italian dishes for our guests.<br />
                You can order brekfast, lunch or dinner.<br /> To book a table please press button "Reserve a Table".</i><br></br><br></br>
                    <button
                        className="bottom-button"
                        onClick={() => window.location.href = '/BookingPage'}>Order a Table</button>
                </h6>
                    </div>
                <img className="header-image" src={restauranfood} alt="Delicious restaurant food" />


        </div>
    );
}

export default Header;