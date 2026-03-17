# Rest API Design
## API Endpoints

### Properties
- `POST /api/v1/properties`: Create a new property
- `GET /api/v1/properties`: List all properties
<!-- To be developed -->
- `GET /api/v1/properties/types/{type_id}` : Get all properties of a specific type 
- `GET /api/v1/properties/{id}`: Get a specific property
- `PATCH /api/v1/properties/{id}`: Update a property
- `DELETE /api/v1/properties/{id}`: Delete a property

### Nodes
- `GET /api/v1/properties/{property_id}/nodes/tree`: Get the property tree
- `GET /api/v1/nodes/{node_id}`: Get a specific node
- `PATCH /api/v1/nodes/{node_id}`: Update a node
- `DELETE /api/v1/nodes/{id}`: Delete a node

### Building Node
- `POST /api/v1//properties/{property_id}/buildings` : Create a new building node
- `GET /api/v1/nodes/{node_id}/building` : Get a specific building node
- `PATCH /api/v1/nodes/{node_id}/building`: Update a building node

### Wing Node
- `POST /api/v1/nodes/{parent_node_id}/wings`: Create a new wing node
- `GET /api/v1/nodes/{node_id}/wing`: Get a specific wing node
- `PATCH /api/v1/nodes/{node_id}/wing`: Update a wing node

### Floor Node
- `POST /api/v1/nodes/{parent_node_id}/floors`: Create a new floor node
- `GET /api/v1/nodes/{node_id}/floor`: Get a specific floor node
- `PATCH /api/v1/nodes/{node_id}/floor`: Update a floor node

### Unit Node
- `POST /api/v1/nodes/{parent_node_id}/units`: Create a new unit node
- `GET /api/v1/nodes/{node_id}/unit`: Get a specific unit node
- `PATCH /api/v1/nodes/{node_id}/unit`: Update a unit node