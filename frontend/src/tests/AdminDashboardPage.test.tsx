import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import AdminDashboardPage from '@pages/AdminDashboardPage';

vi.mock('@api/admin', () => ({
  adminApi: {
    listUsers: vi.fn(),
    listOrders: vi.fn(),
    listActivityLogs: vi.fn(),
  },
}));

import { adminApi } from '@api/admin';

describe('AdminDashboardPage', () => {
  beforeEach(() => {
    vi.mocked(adminApi.listUsers).mockResolvedValue({
      status: 200,
      data: {
        users: [
          {
            id: 'user-1',
            email: 'admin@example.com',
            username: 'admin',
            full_name: 'Admin User',
            role: 'admin',
            is_active: true,
            created_at: '2026-05-18T00:00:00Z',
            updated_at: '2026-05-18T00:00:00Z',
          },
        ],
      },
    });
    vi.mocked(adminApi.listOrders).mockResolvedValue({
      status: 200,
      data: {
        orders: [
          {
            id: 'order-1',
            user_id: 'user-1',
            status: 'processing',
            total_amount: 49.99,
            created_at: '2026-05-18T00:00:00Z',
            updated_at: '2026-05-18T00:00:00Z',
          },
        ],
      },
    });
    vi.mocked(adminApi.listActivityLogs).mockResolvedValue({
      status: 200,
      data: {
        logs: [
          {
            id: 'log-1',
            admin_user_id: 'user-1',
            action: 'create_product',
            resource_type: 'product',
            resource_id: 'product-1',
            details: null,
            ip_address: '127.0.0.1',
            timestamp: '2026-05-18T00:00:00Z',
          },
        ],
      },
    });
  });

  it('renders backend-backed admin dashboard data', async () => {
    render(
      <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <AdminDashboardPage />
      </MemoryRouter>
    );

    expect(await screen.findByRole('heading', { name: /Admin Dashboard/i })).toBeInTheDocument();
    expect(screen.getByText('Admin User')).toBeInTheDocument();
    expect(screen.getByText('order-1'.slice(0, 8))).toBeInTheDocument();
    expect(screen.getByText('create_product')).toBeInTheDocument();
  });
});