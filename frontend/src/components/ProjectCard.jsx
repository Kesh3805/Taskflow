import { useNavigate } from 'react-router-dom';
import { Folder, Users, CheckSquare } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

export default function ProjectCard({ project }) {
  const navigate = useNavigate();

  return (
    <Card 
      className="cursor-pointer transition-all hover:shadow-lg hover:-translate-y-1"
      onClick={() => navigate(`/projects/${project.id}`)}
    >
      <CardHeader>
        <div className="flex items-center gap-2 mb-2">
          <Folder className="h-5 w-5 text-primary" />
          <CardTitle className="text-lg">{project.name}</CardTitle>
        </div>
        <CardDescription className="line-clamp-1">
          {project.description || 'No description'}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-4 text-sm text-muted-foreground border-t pt-4">
          <div className="flex items-center gap-1.5">
            <CheckSquare className="h-4 w-4" />
            <span>{project.task_count} tasks</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Users className="h-4 w-4" />
            <span>{project.members?.length || 0} members</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
