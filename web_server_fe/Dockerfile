FROM node as build-stage

COPY . /workdir
WORKDIR /workdir

# Install node
RUN npm install
RUN npm run build

FROM nginx
COPY --from=build-stage /workdir/dist/ /usr/share/nginx/html