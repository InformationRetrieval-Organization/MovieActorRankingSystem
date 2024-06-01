"use client";
import { Tabs, Tab } from "@nextui-org/react";
import SearchComponent from "./components/SearchComponent";


export default function Home() {
  return (
    <Tabs color="primary"
      variant="underlined"
      size="lg"
      aria-label="Options"
      fullWidth>
      <SearchComponent />
    </Tabs>
  );
}