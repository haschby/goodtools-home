FROM node:22-alpine AS builder

EXPOSE 3000
WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:22-alpine AS runner

ENV NODE_ENV=production
COPY --from=builder /app ./

CMD ["npm", "start"]