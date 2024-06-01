import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardBody, Link, Pagination } from "@nextui-org/react";

export default function ResultsList({ results }: { results: ActorResult[] }) {
    const [currentPage, setCurrentPage] = useState(1);
    const [searchPerformed, setSearchPerformed] = useState(false);
    const [initialRender, setInitialRender] = useState(true);
    const resultsPerPage = 10;

    // Calculate the range of results for the current page
    const startIndex = (currentPage - 1) * resultsPerPage;
    const endIndex = startIndex + resultsPerPage;
    const resultsForPage = results.slice(startIndex, endIndex);

    // On the initial render, it sets initialRender to false.
    // On subsequent renders (when results change), it sets searchPerformed to true.
    useEffect(() => {
        if (initialRender) {
            setInitialRender(false);
        } else {
            setSearchPerformed(true);
        }
    }, [results]);

    // If the search was performed and no results were found, display a message
    if (searchPerformed && results.length === 0) {
        return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Nothing found</div>
    }

    return (
        <div>
            {resultsForPage.map((result, index) => (
                <Card key={index} className="mt-3">
                    <CardBody className="px-3 py-0 text-small text-default-400 mb-2">
                        <p>{result.name}</p>
                    </CardBody>
                </Card>
            ))}
            <Pagination
                className="mt-3"
                total={Math.ceil(results.length / resultsPerPage)}
                initialPage={1}
                onChange={(page) => setCurrentPage(page)}
            />
        </div>
    );
}