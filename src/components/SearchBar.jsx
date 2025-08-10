import React from "react";
import { Box, TextField, FormControl, InputLabel, Select, MenuItem, Button } from "@mui/material";

export default function SearchBar({ searchTerm, setSearchTerm, field, setField, onSearch }) {
  return (
    <Box display="flex" alignItems="center" gap={2}>
      <TextField
        label="Search term..."
        variant="outlined"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
        sx={{ flex: 1 }}
      />
      <FormControl variant="outlined">
        <InputLabel>Field</InputLabel>
        <Select
          value={field}
          onChange={e => setField(e.target.value)}
          label="Field"
          sx={{ minWidth: 120 }}
        >
          <MenuItem value="all">All fields</MenuItem>
          <MenuItem value="title">Title</MenuItem>
          <MenuItem value="author">Author</MenuItem>
        </Select>
      </FormControl>
      <Button variant="contained" color="primary" onClick={onSearch}>
        Search
      </Button>
    </Box>
  );
}