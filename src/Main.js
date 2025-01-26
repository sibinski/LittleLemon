import { Routes, Route } from "react-router-dom";
import HomePage from "./HomePage";
import BookingPage from "./BookingPage";
import Menu from "./Menu"

function Main() {
    return (
            <Routes>
                <Route path="/HomePage" element={<HomePage />}></Route>
            <Route path="/BookingPage" element={<BookingPage />}></Route>
            <Route path="/Menu" element={<Menu />}></Route>
            </Routes>

    );
  }

  export default Main;