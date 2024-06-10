"use server";
const baseUrl = process.env.MAR_API_URL;

export async function getActors(query: string): Promise<ActorModel[]> {  
    try {
        console.log(`fetch actors with: ${baseUrl}/search/classifier/actor?q=${encodeURIComponent(query)}`);

        const response = await fetch(`${baseUrl}/search/classifier/actor?q=${encodeURIComponent(query)}`);

        const data = await response.json();
        const actors: ActorModel[] = data as ActorModel[];

        return actors;
    } catch (error) {
        console.error(`Error fetching actors: ${error}`);
        return [];
    }
}
