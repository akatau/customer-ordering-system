# Phase 1: Requirement Discovery & Traceability

## Actor Classification

Actors are classified based on their interaction with the system as per use case modeling standards.

### Primary Actors
Primary actors initiate the core use cases of the system. They are the main users whose goals the system is designed to fulfill.

- **Customer**: An individual or business entity who browses products, manages a shopping cart, places orders, and tracks order status. The system exists primarily to serve customers.

### Supporting Actors
Supporting actors provide assistance or secondary services to the primary actors. They interact with the system to enable or enhance the primary use cases.

- **System Administrator**: A privileged user who manages the system's configuration, including adding/removing products, managing user accounts, and generating reports. Supports the overall operation of the system.
- **Customer Support Representative**: A user who handles customer inquiries, order modifications, refunds, and issue resolution. Provides secondary support to customers.

### Offstage Actors
Offstage actors are external systems or entities that the system interacts with but are not directly controlled by the system. They represent external dependencies.

- **Payment Gateway**: An external service (e.g., Stripe, PayPal) that processes payment transactions securely.
- **Inventory Management System**: An external system that tracks product stock levels and availability.
- **Shipping Provider**: An external service (e.g., UPS, FedEx) that handles order fulfillment and delivery tracking.
- **Email Service**: An external service for sending order confirmations, notifications, and marketing emails.

### Actor Interactions Summary
- Primary actors drive the business value.
- Supporting actors enable system maintenance and customer service.
- Offstage actors provide essential external capabilities without which the system cannot function independently.

This classification ensures that all system interactions are accounted for in design and testing.
