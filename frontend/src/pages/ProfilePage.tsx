/**
 * User profile page component
 */

import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Divider,
  Tabs,
  Tab,
} from '@mui/material';
import { useAuthStore } from '@stores/authStore';
import { userApi } from '@api/users';
import { UserProfile } from '@/types';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index } = props;
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ pt: 2 }}>{children}</Box>}
    </div>
  );
}

const ProfilePage: React.FC = () => {
  const { user } = useAuthStore();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [activeTab, setActiveTab] = useState(0);

  // Profile form state
  const [profileData, setProfileData] = useState({
    full_name: '' as string | null,
    phone: '',
  });

  // Password form state
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setIsLoading(true);
    const response = await userApi.getProfile();

    if (response.error) {
      setError(response.error.detail);
    } else if (response.data) {
      setProfile(response.data);
      setProfileData({
        full_name: response.data.full_name,
        phone: response.data.phone || '',
      });
    }
    setIsLoading(false);
  };

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfileData((prev) => ({ ...prev, [name]: value }));
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setPasswordData((prev) => ({ ...prev, [name]: value }));
  };

  const handleUpdateProfile = async () => {
    setError('');
    setSuccess('');
    setIsSaving(true);

    const response = await userApi.updateProfile({
      full_name: profileData.full_name,
      phone: profileData.phone,
    });

    if (response.error) {
      setError(response.error.detail);
    } else {
      setSuccess('Profile updated successfully!');
      loadProfile();
    }
    setIsSaving(false);
  };

  const handleChangePassword = async () => {
    setError('');
    setSuccess('');

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (passwordData.newPassword.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setIsSaving(true);

    const response = await userApi.changePassword(
      passwordData.currentPassword,
      passwordData.newPassword
    );

    if (response.error) {
      setError(response.error.detail);
    } else {
      setSuccess('Password changed successfully!');
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
    }
    setIsSaving(false);
  };

  if (isLoading) {
    return <CircularProgress sx={{ display: 'block', mx: 'auto' }} />;
  }

  if (!profile) {
    return <Alert severity="error">Failed to load profile</Alert>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        My Account
      </Typography>

      <Paper sx={{ mb: 3 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
            <Tab label="Profile" />
            <Tab label="Change Password" />
            <Tab label="Account Info" />
          </Tabs>
        </Box>

        {error && <Alert severity="error" sx={{ m: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ m: 2 }}>{success}</Alert>}

        <TabPanel value={activeTab} index={0}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Edit Profile
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <TextField
              fullWidth
              label="Full Name"
              name="full_name"
              value={profileData.full_name}
              onChange={handleProfileChange}
              margin="normal"
              disabled={isSaving}
            />

            <TextField
              fullWidth
              label="Email"
              value={profile.email}
              disabled
              margin="normal"
              helperText="Email cannot be changed"
            />

            <TextField
              fullWidth
              label="Phone"
              name="phone"
              value={profileData.phone}
              onChange={handleProfileChange}
              margin="normal"
              disabled={isSaving}
            />

            <Button
              variant="contained"
              color="primary"
              onClick={handleUpdateProfile}
              sx={{ mt: 2 }}
              disabled={isSaving}
            >
              {isSaving ? 'Saving...' : 'Save Changes'}
            </Button>
          </Box>
        </TabPanel>

        <TabPanel value={activeTab} index={1}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Change Password
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <TextField
              fullWidth
              label="Current Password"
              name="currentPassword"
              type="password"
              value={passwordData.currentPassword}
              onChange={handlePasswordChange}
              margin="normal"
              disabled={isSaving}
            />

            <TextField
              fullWidth
              label="New Password"
              name="newPassword"
              type="password"
              value={passwordData.newPassword}
              onChange={handlePasswordChange}
              margin="normal"
              disabled={isSaving}
              helperText="At least 8 characters"
            />

            <TextField
              fullWidth
              label="Confirm Password"
              name="confirmPassword"
              type="password"
              value={passwordData.confirmPassword}
              onChange={handlePasswordChange}
              margin="normal"
              disabled={isSaving}
            />

            <Button
              variant="contained"
              color="primary"
              onClick={handleChangePassword}
              sx={{ mt: 2 }}
              disabled={isSaving}
            >
              {isSaving ? 'Updating...' : 'Change Password'}
            </Button>
          </Box>
        </TabPanel>

        <TabPanel value={activeTab} index={2}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Account Information
            </Typography>
            <Divider sx={{ mb: 2 }} />

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Box>
                <Typography variant="body2" color="textSecondary">
                  User ID
                </Typography>
                <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                  {profile.id}
                </Typography>
              </Box>

              <Box>
                <Typography variant="body2" color="textSecondary">
                  Email
                </Typography>
                <Typography variant="body1">{profile.email}</Typography>
              </Box>

              <Box>
                <Typography variant="body2" color="textSecondary">
                  Account Created
                </Typography>
                <Typography variant="body1">
                  {new Date(profile.created_at).toLocaleDateString()}
                </Typography>
              </Box>

              <Box>
                <Typography variant="body2" color="textSecondary">
                  Role
                </Typography>
                <Typography variant="body1">{user?.role || 'Customer'}</Typography>
              </Box>
            </Box>
          </Box>
        </TabPanel>
      </Paper>
    </Box>
  );
};

export default ProfilePage;
