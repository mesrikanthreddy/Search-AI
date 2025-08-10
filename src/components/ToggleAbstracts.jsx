import React from "react";
import { Box, FormControl, RadioGroup, FormControlLabel, Radio } from "@mui/material";

export default function ToggleAbstracts({ showAbstract, setShowAbstract }) {
  return (
    <Box mt={2}>
      <FormControl component="fieldset">
        <RadioGroup
          row
          value={showAbstract ? "show" : "hide"}
          onChange={e => setShowAbstract(e.target.value === "show")}
        >
          <FormControlLabel value="show" control={<Radio />} label="Show abstracts" />
          <FormControlLabel value="hide" control={<Radio />} label="Hide abstracts" />
        </RadioGroup>
      </FormControl>
    </Box>
  );
}