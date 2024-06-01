"use client";
import React, { useEffect, useState } from "react";
import { Button, Divider, Input } from "@nextui-org/react";
import { SearchIcon } from "../../components/icons";
import ResultsList from "./ResultsList";
import { getActors } from '../api/movieActorRanking';

const SearchComponent = () => {
    const [inputValue, setInputValue] = useState("");
    const [results, setResults] = useState<ActorResult[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    const fetchData = async () => {
        setIsLoading(true);

        try {
            let url = '';
            let data: ActorResult[] = [];

            url = `/search/actor?q=${inputValue.replace(/\s/g, '+')}`;
            data = await getActors(url);

            setResults(data);
        } catch (error) {
            console.error("Failed to fetch data:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <section className="flex flex-col gap-5 m-8">
            <div className="flex items-center gap-2">
                <Input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="search term"
                    size="md"
                    type="search"
                />

                <Button isIconOnly color="primary" variant="solid" size="lg" onClick={fetchData} isLoading={isLoading}>
                    <SearchIcon size={18} />
                </Button>
            </div>

            <Divider />

            <ResultsList results={results} />
        </section>
    );
}

export default SearchComponent;