import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import AdvancedSearchPage from "./pages/AdvancedSearchPage";
import FileUpload from './components/FileUpload';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/advanced-search" element={<AdvancedSearchPage />} />
      </Routes>
      <FileUpload />
    </Router>
  );
}

export default App;