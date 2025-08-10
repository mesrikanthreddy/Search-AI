import React, { useState } from "react";
import { Box, Typography, Link } from "@mui/material";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import ToggleAbstracts from "../components/ToggleAbstracts";

export default function SearchPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [field, setField] = useState("all");
  const [showAbstract, setShowAbstract] = useState(true);

  const handleSearch = () => {
    // Implement your search logic here
    alert(`Searching for "${searchTerm}" in "${field}" fields. Show abstracts: ${showAbstract}`);
  };

  return (
    <div>
      <Header />
      <Box sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Search
        </Typography>
        <SearchBar
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          field={field}
          setField={setField}
          onSearch={handleSearch}
        />
        <ToggleAbstracts showAbstract={showAbstract} setShowAbstract={setShowAbstract} />
        <Box mt={2}>
          <Link href="/advanced-search" underline="hover">
            Advanced Search
          </Link>
        </Box>
      </Box>
    </div>
  );
}