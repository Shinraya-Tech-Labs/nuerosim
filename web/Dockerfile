FROM node:22.23.0-bookworm-slim
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY web/package*.json ./
RUN npm ci
COPY web/ ./
ARG NEUROSIM_API_URL=http://neurosim:8000
ENV NEUROSIM_API_URL=$NEUROSIM_API_URL
RUN npm run build && npm prune --omit=dev
USER node
EXPOSE 3000
CMD ["node", "node_modules/next/dist/bin/next", "start", "--hostname", "0.0.0.0"]
