# Customer Ordering System - Frontend

A modern React TypeScript web application for the Customer Ordering System built with Vite and Material-UI.

## Features

- ✅ User Authentication (Register/Login)
- ✅ Product Catalog with Search & Filtering
- ✅ Product Details & Reviews
- ✅ Shopping Cart Management
- ✅ Checkout Flow (Shipping, Billing, Payment)
- ✅ Order Management & Tracking
- ✅ User Profile Management
- ✅ Responsive Design (Mobile/Tablet/Desktop)
- ✅ Material-UI Components
- ✅ State Management with Zustand
- ✅ TypeScript for Type Safety

## Tech Stack

- **Frontend Framework**: React 18.2
- **Language**: TypeScript 5.2
- **Build Tool**: Vite 4.5
- **UI Library**: Material-UI (MUI) 5.14
- **State Management**: Zustand 4.4
- **Form Handling**: React Hook Form 7.48
- **HTTP Client**: Axios 1.6
- **Routing**: React Router DOM 6.18
- **Testing**: Vitest + React Testing Library
- **Styling**: Emotion (MUI's recommended CSS-in-JS)

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API service clients
│   │   ├── client.ts     # Base API client with interceptors
│   │   ├── auth.ts       # Authentication endpoints
│   │   ├── products.ts   # Product endpoints
│   │   ├── cart.ts       # Cart endpoints
│   │   ├── orders.ts     # Order endpoints
│   │   └── users.ts      # User profile endpoints
│   ├── components/       # Reusable components
│   │   ├── Header.tsx    # Navigation header
│   │   └── Footer.tsx    # Footer
│   ├── pages/            # Page components
│   │   ├── HomePage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── ProductCatalogPage.tsx
│   │   ├── ProductDetailPage.tsx
│   │   ├── CartPage.tsx
│   │   ├── CheckoutPage.tsx
│   │   ├── OrdersPage.tsx
│   │   ├── OrderTrackingPage.tsx
│   │   └── ProfilePage.tsx
│   ├── stores/           # Zustand state management
│   │   ├── authStore.ts
│   │   ├── cartStore.ts
│   │   ├── productsStore.ts
│   │   └── ordersStore.ts
│   ├── types/            # TypeScript type definitions
│   │   └── index.ts
│   ├── utils/            # Utility functions
│   ├── tests/            # Test setup
│   ├── App.tsx           # Root component with routing
│   ├── main.tsx          # Entry point
│   └── index.css         # Global styles
├── public/               # Static assets
├── package.json
├── tsconfig.json
├── vite.config.ts
├── vitest.config.ts
├── .eslintrc.cjs
├── .prettierrc
└── index.html
```

## Installation & Setup

### Prerequisites
- Node.js 20+
- npm or yarn

### Setup

1. **Install dependencies**:
```bash
cd frontend
yarn install
# or
npm install
```

2. **Create environment file**:
```bash
cp .env.example .env.local
```

Configure the API URL:
```
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

3. **Start development server**:
```bash
yarn dev
# or
npm run dev
```

The application will be available at `http://localhost:5173`

## Available Scripts

- `yarn dev` - Start development server
- `yarn build` - Build for production
- `yarn preview` - Preview production build locally
- `yarn test` - Run tests
- `yarn test:coverage` - Run tests with coverage report
- `yarn lint` - Run ESLint
- `yarn type-check` - Run TypeScript type checking
- `yarn format` - Format code with Prettier

## API Integration

The frontend consumes APIs from the backend at:
```
http://localhost:8000/api/v1
```

All API endpoints are documented with OpenAPI/Swagger at:
```
http://localhost:8000/docs
```

### Authentication Flow

1. User registers or logs in
2. Backend returns JWT token
3. Token is stored in localStorage
4. Token is automatically included in all subsequent requests
5. On token expiration (401), user is redirected to login

### API Client Usage

```typescript
import { apiClient } from '@api/client';

// Set token after login
apiClient.setToken(token);

// Make requests
const response = await productApi.listProducts();

// Token is automatically included in Authorization header
```

## State Management

The application uses Zustand for simple and efficient state management:

### Auth Store
- Manages user authentication state
- Handles login/register/logout
- Persists token to localStorage

### Cart Store
- Manages shopping cart state
- Handles add/remove/update operations
- Persists cart across sessions

### Products Store
- Manages product catalog state
- Handles product list and detail fetching
- Manages search and filter state

### Orders Store
- Manages user orders state
- Handles order creation and retrieval
- Manages order tracking

## Testing

Run tests with:
```bash
yarn test
```

Run tests with coverage:
```bash
yarn test:coverage
```

Coverage reports are generated in `coverage/` directory.

## Performance Optimizations

- Code splitting with React Router
- Lazy loading of pages
- Image optimization
- CSS-in-JS with Emotion (automatic critical CSS)
- Memoization of components where appropriate
- Efficient state updates with Zustand

## Accessibility (WCAG 2.1 AA)

The application follows accessibility best practices:
- Semantic HTML elements
- Proper ARIA labels
- Keyboard navigation support
- Color contrast compliance
- Screen reader support
- Focus management

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

## Deployment

### Build for Production

```bash
yarn build
```

This creates an optimized build in the `dist/` directory.

### Environment Variables

Set these for production deployment:
```
VITE_API_URL=https://api.yourdomain.com
VITE_API_TIMEOUT=30000
```

### Serving the Build

The built files can be served with any static file server:
```bash
yarn preview
# or
npx serve dist
```

## Troubleshooting

### API Connection Issues
- Verify backend is running on `http://localhost:8000`
- Check `VITE_API_URL` environment variable
- Check browser console for CORS errors

### State Not Persisting
- Check localStorage is enabled
- Verify browser isn't in private/incognito mode
- Clear localStorage if having issues: `localStorage.clear()`

### Build Issues
- Clear node_modules and reinstall: `rm -rf node_modules && yarn install`
- Clear Vite cache: `rm -rf node_modules/.vite`

## Contributing

When adding new features:
1. Create a new branch: `git checkout -b feature/feature-name`
2. Follow the project structure
3. Write tests for new functionality
4. Run `yarn lint` and `yarn type-check` before committing
5. Create a pull request

## Documentation

- [Design Documentation](../docs/final_design.md)
- [API Contracts](../docs/api_contracts.md)
- [User Stories](../docs/user_stories.md)
- [Requirements](../docs/requirements.md)

## License

Proprietary - Customer Ordering System
