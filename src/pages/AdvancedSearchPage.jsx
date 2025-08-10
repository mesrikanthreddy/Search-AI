import React from "react";
import { Box, Typography } from "@mui/material";
import Header from "../components/Header";

export default function AdvancedSearchPage() {
  return (
    <div>
      <Header />
      <Box sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Advanced Search
        </Typography>
        {/* Add your advanced search form here */}
        <Typography>Coming soon...</Typography>
      </Box>
    </div>
  );
}