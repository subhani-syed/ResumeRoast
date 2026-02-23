# ---------- Base Image ----------
FROM node:20-alpine AS base
WORKDIR /app

# ---------- Dependencies ----------
FROM base AS deps
COPY package.json package-lock.json ./
RUN npm ci

# ---------- Build ----------
FROM base AS builder
ARG NEXT_PUBLIC_API_URL
ARG INTERNAL_API_URL
ARG IMAGE_HOSTNAME
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV INTERNAL_API_URL=$INTERNAL_API_URL
ENV IMAGE_HOSTNAME=$IMAGE_HOSTNAME

COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# ---------- Production Runner ----------
FROM node:20-alpine AS runner

WORKDIR /app
RUN addgroup -S nextjs && adduser -S nextjs -G nextjs

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

USER nextjs

EXPOSE 3000

CMD ["node", "server.js"]
