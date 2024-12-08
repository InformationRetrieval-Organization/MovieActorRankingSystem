interface RoleModel {
    id: number;
    name: string;
    movieId: number;
    movie: MovieModel;
    actor: ActorModel;
    actorId: number;
    //scripts: Script[];
}