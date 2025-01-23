import React from 'react';
import { Card, CardContent, CardActions, Typography, IconButton } from '@mui/material';
import { Favorite, Comment as CommentIcon } from '@mui/icons-material';
import { Post as PostType } from '../../types';

interface Props {
  post: PostType;
  onLike: (postId: string) => void;
  onComment: (postId: string) => void;
}

export const Post: React.FC<Props> = ({ post, onLike, onComment }) => {
  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="body1">{post.content}</Typography>
      </CardContent>
      <CardActions>
        <IconButton onClick={() => onLike(post.id)}>
          <Favorite color={post.liked ? "error" : "inherit"} />
        </IconButton>
        <Typography variant="body2">{post.likes}</Typography>
        <IconButton onClick={() => onComment(post.id)}>
          <CommentIcon />
        </IconButton>
        <Typography variant="body2">{post.comments.length}</Typography>
      </CardActions>
    </Card>
  );
}; 