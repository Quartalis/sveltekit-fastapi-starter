FROM node:20-slim AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20-slim

WORKDIR /app

# adapter-node bundles every devDependency into build/, so the runtime image
# needs no node_modules (add them back if you add runtime `dependencies`).
COPY --from=build /app/build build/
COPY package.json .

EXPOSE 3000
ENV NODE_ENV=production

CMD ["node", "build"]
