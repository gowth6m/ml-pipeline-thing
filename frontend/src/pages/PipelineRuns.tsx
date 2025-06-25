
import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { RunHistory } from "@/components/RunHistory";
import { Pipeline, PipelineRun } from "@/types/pipeline";
import { api } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { AlertCircle, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";

const PipelineRuns = () => {
  const { pipelineId } = useParams<{ pipelineId: string }>();
  const navigate = useNavigate();

  // Get pipeline details
  const { 
    data: pipeline, 
    isLoading: pipelineLoading, 
    error: pipelineError 
  } = useQuery({
    queryKey: ['pipeline', pipelineId],
    queryFn: () => api.pipelines.get(pipelineId!),
    enabled: !!pipelineId,
    retry: 2,
  });

  const handleSelectRun = (run: PipelineRun) => {
    console.log('Selected run:', run);
    // Could navigate to a run detail page in the future
    // navigate(`/pipeline/${pipelineId}/runs/${run.id}`);
  };

  const handleBackToPipeline = () => {
    navigate(`/pipeline/${pipelineId}`);
  };

  if (pipelineError) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={handleBackToPipeline}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Pipeline
          </Button>
        </div>
        
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Failed to load pipeline. {pipelineError.message}
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  if (pipelineLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={handleBackToPipeline}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Pipeline
          </Button>
        </div>
        
        <Card className="animate-pulse">
          <CardContent className="p-6">
            <div className="space-y-4">
              <div className="h-8 bg-gray-200 rounded w-1/3"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-20 bg-gray-200 rounded"></div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!pipeline) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={handleBackToPipeline}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Pipeline
          </Button>
        </div>
        
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Pipeline not found.
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" onClick={handleBackToPipeline}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Pipeline
        </Button>
      </div>
      
      <RunHistory
        pipeline={pipeline as Pipeline}
        onSelectRun={handleSelectRun}
      />
    </div>
  );
};

export default PipelineRuns;
