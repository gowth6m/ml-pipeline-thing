import { useQuery } from "@tanstack/react-query";
import { Clock, CheckCircle, XCircle, Play, Calendar, AlertCircle } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Pipeline, PipelineRun } from "@/types/pipeline";
import { api } from "@/lib/api";

interface RunHistoryProps {
  pipeline: Pipeline;
  onSelectRun: (run: PipelineRun) => void;
}

export function RunHistory({ pipeline, onSelectRun }: RunHistoryProps) {
  const { 
    data: runsData, 
    isLoading, 
    error,
    refetch 
  } = useQuery({
    queryKey: ['pipeline-runs', pipeline.id],
    queryFn: () => api.runs.list(pipeline.id),
    retry: 2,
    staleTime: 30000,
  });

  const runs = runsData?.items || [];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case "failed":
        return <XCircle className="w-4 h-4 text-red-600" />;
      case "running":
        return <Clock className="w-4 h-4 text-blue-600 animate-spin" />;
      case "pending":
        return <Clock className="w-4 h-4 text-yellow-600" />;
      case "cancelled":
        return <XCircle className="w-4 h-4 text-gray-600" />;
      default:
        return <Clock className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "bg-green-100 text-green-700";
      case "failed":
        return "bg-red-100 text-red-700";
      case "running":
        return "bg-blue-100 text-blue-700";
      case "pending":
        return "bg-yellow-100 text-yellow-700";
      case "cancelled":
        return "bg-gray-100 text-gray-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDuration = (startStr: string | null, endStr?: string | null) => {
    if (!startStr) return 'N/A';
    const start = new Date(startStr);
    const end = endStr ? new Date(endStr) : new Date();
    const diffMs = end.getTime() - start.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    
    if (diffHours > 0) {
      return `${diffHours}h ${diffMins % 60}m`;
    }
    return `${diffMins}m`;
  };

  if (error) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Run History</h1>
            <p className="text-gray-600 mt-1">
              Execution history for pipeline: <span className="font-medium">{pipeline.name}</span>
            </p>
          </div>
        </div>
        
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Failed to load pipeline runs. {error.message}
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => refetch()} 
              className="ml-2"
            >
              Retry
            </Button>
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Run History</h1>
          <p className="text-gray-600 mt-1">
            Execution history for pipeline: <span className="font-medium">{pipeline.name}</span>
          </p>
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4" />
            <span>{isLoading ? '...' : runs.length} total runs</span>
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="grid gap-4">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </CardHeader>
              <CardContent>
                <div className="h-16 bg-gray-200 rounded"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="grid gap-4">
        {runs.length === 0 ? (
          <Card className="bg-white/90 backdrop-blur-sm">
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Play className="w-12 h-12 text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No runs yet</h3>
              <p className="text-gray-500 text-center">
                This pipeline hasn't been executed yet. Trigger a run to see execution history here.
              </p>
            </CardContent>
          </Card>
        ) : (
          runs.map((run) => (
            <Card 
              key={run.id} 
              className="hover:shadow-lg transition-all duration-200 bg-white/90 backdrop-blur-sm cursor-pointer"
              onClick={() => onSelectRun(run)}
            >
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {getStatusIcon(run.status)}
                    <div>
                      <CardTitle className="text-lg">Run #{run.runId}</CardTitle>
                      <CardDescription>
                        Started {formatDate(run.startedAt)}
                      </CardDescription>
                    </div>
                  </div>
                  <Badge className={getStatusColor(run.status)}>
                    {run.status.charAt(0).toUpperCase() + run.status.slice(1)}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-gray-500">Duration:</span>
                    <div className="font-medium">
                      {run.completedAt 
                        ? formatDuration(run.startedAt, run.completedAt)
                        : run.status === "running" 
                          ? formatDuration(run.startedAt) + " (ongoing)"
                          : "N/A"
                      }
                    </div>
                  </div>
                  
                  <div>
                    <span className="text-gray-500">Environment:</span>
                    <div className="font-medium">{run.environment}</div>
                  </div>
                  
                  <div>
                    <span className="text-gray-500">Trigger:</span>
                    <div className="font-medium">{run.triggerType}</div>
                  </div>

                  {run.executionTime && (
                    <div>
                      <span className="text-gray-500">Execution Time:</span>
                      <div className="font-medium">{Math.round(run.executionTime)}s</div>
                    </div>
                  )}
                </div>

                {run.successCount !== undefined && run.failedCount !== undefined && (
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Success Count:</span>
                      <div className="font-medium text-green-600">{run.successCount}</div>
                    </div>
                    <div>
                      <span className="text-gray-500">Failed Count:</span>
                      <div className="font-medium text-red-600">{run.failedCount}</div>
                    </div>
                  </div>
                )}

                {run.errorMessage && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                    <div className="flex items-center gap-2 text-red-700 text-sm">
                      <XCircle className="w-4 h-4" />
                      <span className="font-medium">Error:</span>
                    </div>
                    <p className="text-red-600 text-sm mt-1">{run.errorMessage}</p>
                  </div>
                )}

                {run.notes && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                    <div className="text-blue-700 text-sm font-medium">Notes:</div>
                    <p className="text-blue-600 text-sm mt-1">{run.notes}</p>
                  </div>
                )}

                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                  {run.completedAt && (
                    <span className="text-sm text-gray-500">
                      Completed {formatDate(run.completedAt)}
                    </span>
                  )}
                  <Button size="sm" variant="outline" onClick={(e) => {
                    e.stopPropagation();
                    onSelectRun(run);
                  }}>
                    View Details
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
      )}
    </div>
  );
}
