import React from 'react';
import { Card, Avatar, Typography, Box } from '@mui/material';
import { AIProfile as ProfileType } from '../../types';

interface Props {
  profile: ProfileType;
}

export const AIProfile: React.FC<Props> = ({ profile }) => {
  return (
    <Card sx={{ p: 2, mb: 2 }}>
      <Box display="flex" alignItems="center">
        <Avatar sx={{ width: 60, height: 60 }}>
          {profile.name[0]}
        </Avatar>
        <Box ml={2}>
          <Typography variant="h6">{profile.name}</Typography>
          <Typography variant="body2" color="text.secondary">
            {profile.bio}
          </Typography>
          <Box mt={1}>
            {profile.interests.map((interest, index) => (
              <Typography key={index} variant="caption" sx={{ mr: 1 }}>
                #{interest}
              </Typography>
            ))}
          </Box>
        </Box>
      </Box>
    </Card>
  );
}; 