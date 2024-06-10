interface MovieModel {
    id: number;
    imdbId: number;
    title: string;
    coverUrl: string;
    roles: RoleModel[];
    //scripts: Script[];
}