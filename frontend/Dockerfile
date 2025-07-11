
# ─── Stage 1 – build React with Vite ───────────────────
FROM node:slim AS builder
WORKDIR /app

# Pass build-time env variable
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# 1) Copy package files and install everything, including dev & optional
COPY package.json package-lock.json ./
RUN npm ci

# 2) Make sure esbuild gets rebuilt for Linux
RUN npm rebuild esbuild

# 3) Copy the rest of your source & build
COPY . .
RUN npm run build

# ─── Stage 2 – serve static with Nginx ────────────────
FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 4) Copy the built files into Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
