import './App.css';
import Home from "./pages/Home";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Movie from "./pages/Movie";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Home/>}/>
          <Route path="/movie/*" element={<Movie/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
