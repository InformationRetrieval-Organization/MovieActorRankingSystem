# Movie Actor Ranking UI
[![Build and deploy container app to Azure Web App - app-movieactorranking-prod](https://github.com/InformationRetrieval-Organization/MovieActorRankingUI/actions/workflows/main_app-movieactorranking-prod.yml/badge.svg)](https://github.com/InformationRetrieval-Organization/MovieActorRankingUI/actions/workflows/main_app-movieactorranking-prod.yml)

## Technologies Used

- [Next.js 13](https://nextjs.org/docs/getting-started)
- [NextUI v2](https://nextui.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Tailwind Variants](https://tailwind-variants.org)
- [TypeScript](https://www.typescriptlang.org/)
- [Framer Motion](https://www.framer.com/motion/)
- [next-themes](https://github.com/pacocoursey/next-themes)

## How to Use

### environment variables
* copy and rename the `.env.sample` file to `.env`

### Install dependencies

```bash
npm install
```

### Run the development server

```bash
npm run dev
```

## deployment
```bash
npm run build
npm run start
```

## optional: Docker
building
```bash
docker build --tag tonylukeregistry.azurecr.io/tonylukeregistry/information-retrieval/ui:latest .
```

running container locally
```bash
docker run --detach --publish 3000:3000 tonylukeregistry.azurecr.io/tonylukeregistry/information-retrieval/ui:latest
```
