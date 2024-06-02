"use server";
const baseUrl = process.env.MAR_API_URL;

export async function getActors(query: string): Promise<ActorResult[]> {  
    try {
        console.log(`fetch actors with: ${baseUrl}/search/actor?q=${encodeURIComponent(query)}`);

        const response = await fetch(`${baseUrl}/search/actor?q=${encodeURIComponent(query)}`);

        const data = await response.json();
        const actors: ActorResult[] = data as ActorResult[];

        return actors;
    } catch (error) {
        console.error(`Error fetching actors: ${error}`);
        return [];
    }
}
