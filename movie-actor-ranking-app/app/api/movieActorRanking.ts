"use server";
const baseUrl = process.env.MAR_API_URL;

export async function getActors(url: string): Promise<ActorResult[]> {  
    try {
        const response = await fetch(`${baseUrl}${url}`);

        const data = await response.json();
        const actors: ActorResult[] = data as ActorResult[];

        return actors;
    } catch (error) {
        console.error(`Error fetching actors: ${error}`);
        return [];
    }
}
