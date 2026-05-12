# UML Modeling

## System Sequence Diagrams

### Happy Path: Successful Order Placement

```mermaid
sequenceDiagram
    participant C as Customer
    participant S as System
    participant I as Inventory
    participant P as Payment Gateway
    participant SH as Shipping
    participant E as Email Service

    C->>S: Browse products
    S-->>C: Return product catalog
    C->>S: Add items to cart
    S-->>C: Confirm cart update
    C->>S: Initiate checkout
    S-->>C: Show order summary
    C->>S: Submit order with payment info
    S->>I: Check inventory availability
    I-->>S: Confirm stock available
    S->>P: Process payment
    P-->>S: Payment successful
    S->>S: Create order record
    S->>SH: Schedule shipping
    SH-->>S: Shipping confirmed
    S->>E: Send confirmation email
    E-->>S: Email sent
    S-->>C: Return order confirmation
```

### Failure Path: Payment Declines

```mermaid
sequenceDiagram
    participant C as Customer
    participant S as System
    participant I as Inventory
    participant P as Payment Gateway

    C->>S: Submit order with payment info
    S->>I: Check inventory availability
    I-->>S: Confirm stock available
    S->>P: Process payment
    P-->>S: Payment declined
    S->>S: Log payment failure
    S-->>C: Return payment error message
    Note over C,S: Cart remains intact for retry
```

### Failure Path: Insufficient Inventory

```mermaid
sequenceDiagram
    participant C as Customer
    participant S as System
    participant I as Inventory

    C->>S: Submit order with payment info
    S->>I: Check inventory availability
    I-->>S: Insufficient stock for item X
    S->>S: Update cart with available quantities
    S-->>C: Return inventory error with suggestions
    Note over C,S: Customer can adjust cart or cancel
```

## Activity Diagrams

### Order Placement Process with Code Decision Points

```mermaid
stateDiagram-v2
    [*] --> BrowseCatalog
    BrowseCatalog --> AddToCart: User selects product
    AddToCart --> UpdateCart: Code: validate_quantity()
    UpdateCart --> BrowseCatalog: Continue shopping
    UpdateCart --> Checkout: Proceed to checkout
    Checkout --> ValidateCart: Code: check_cart_validity()
    ValidateCart --> CartError: Code: if empty or invalid
    CartError --> [*]
    ValidateCart --> CollectShipping: Code: if valid
    CollectShipping --> CollectPayment: User enters details
    CollectPayment --> ProcessOrder: User submits
    ProcessOrder --> CheckInventory: Code: inventory_service.check_stock()
    CheckInventory --> InventoryFail: Code: if insufficient
    InventoryFail --> NotifyCustomer: Code: send_inventory_error()
    NotifyCustomer --> [*]
    CheckInventory --> ProcessPayment: Code: if available
    ProcessPayment --> PaymentGateway: Code: payment_service.charge()
    PaymentGateway --> PaymentSuccess: Code: if approved
    PaymentSuccess --> CreateOrder: Code: order_service.create()
    CreateOrder --> ScheduleShipping: Code: shipping_service.schedule()
    ScheduleShipping --> SendConfirmation: Code: email_service.send()
    SendConfirmation --> OrderComplete: Code: return_success()
    OrderComplete --> [*]
    PaymentGateway --> PaymentFail: Code: if declined
    PaymentFail --> NotifyPaymentError: Code: send_payment_error()
    NotifyPaymentError --> [*]
```

### User Authentication Flow

```mermaid
stateDiagram-v2
    [*] --> LoginPage
    LoginPage --> ValidateInput: User submits credentials
    ValidateInput --> InputError: Code: if email/password empty
    InputError --> LoginPage
    ValidateInput --> CheckCredentials: Code: if input valid
    CheckCredentials --> AuthSuccess: Code: if credentials match DB
    AuthSuccess --> CreateSession: Code: session_manager.create()
    CreateSession --> RedirectDashboard: Code: redirect to catalog
    RedirectDashboard --> [*]
    CheckCredentials --> AuthFail: Code: if credentials invalid
    AuthFail --> IncrementAttempts: Code: security_service.check_attempts()
    IncrementAttempts --> LockAccount: Code: if attempts > 5
    LockAccount --> AccountLocked: Code: send_lock_notification()
    AccountLocked --> [*]
    IncrementAttempts --> ShowError: Code: if attempts <= 5
    ShowError --> LoginPage
```

## Design Decisions

### Sequence Diagram Choices
- **System Boundary**: The "System" participant represents the Customer Ordering sub-system, encapsulating all internal components.
- **Happy Path**: Covers the complete successful flow from browsing to confirmation.
- **Failure Paths**: Include common failure scenarios (payment decline, inventory issues) to ensure robust error handling.
- **External Actors**: Payment Gateway, Inventory, Shipping, and Email are modeled as separate participants to highlight integration points.

### Activity Diagram Choices
- **Code Integration**: Decision points explicitly call out code methods (e.g., `validate_quantity()`, `check_stock()`) to show where business logic resides.
- **State Representation**: Uses states for user interactions and processes for system operations.
- **Error Handling**: Dedicated paths for different error conditions ensure comprehensive coverage.
- **Flow Control**: Guards on transitions represent conditional logic that will be implemented in code.

These diagrams provide visual specifications for implementation and testing, with code-level detail for developers.
