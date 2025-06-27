import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { PipelineView } from "@/components/PipelineView";
import { Pipeline } from "@/types/pipeline";
import { api } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { AlertCircle, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";

const PipelineDetail = () => {
    const { pipelineId } = useParams<{ pipelineId: string }>();
    const navigate = useNavigate();

    const {
        data: pipeline,
        isLoading,
        error,
    } = useQuery({
        queryKey: ["pipeline", pipelineId],
        queryFn: () => api.pipelines.get(pipelineId!),
        enabled: !!pipelineId,
        retry: 2,
    });

    const handleViewRuns = () => {
        navigate(`/pipeline/${pipelineId}/runs`, {
            state: { pipeline: pipeline as Pipeline },
        });
    };

    const handleBackToPipelines = () => {
        navigate("/pipelines");
    };

    if (error) {
        return (
            <div className="space-y-6">
                <div className="flex items-center gap-4">
                    <Button variant="outline" onClick={handleBackToPipelines}>
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back to Pipelines
                    </Button>
                </div>

                <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                        Failed to load pipeline details. {error.message}
                    </AlertDescription>
                </Alert>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="space-y-6">
                <div className="flex items-center gap-4">
                    <Button variant="outline" onClick={handleBackToPipelines}>
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back to Pipelines
                    </Button>
                </div>

                <Card className="animate-pulse">
                    <CardContent className="p-6">
                        <div className="space-y-4">
                            <div className="h-8 bg-gray-200 rounded w-1/3"></div>
                            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                            <div className="h-64 bg-gray-200 rounded"></div>
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
                    <Button variant="outline" onClick={handleBackToPipelines}>
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back to Pipelines
                    </Button>
                </div>

                <Alert>
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>Pipeline not found.</AlertDescription>
                </Alert>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-4">
                <Button variant="outline" onClick={handleBackToPipelines}>
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back to Pipelines
                </Button>
            </div>

            <PipelineView
                pipeline={pipeline as Pipeline}
                onViewRuns={handleViewRuns}
            />
        </div>
    );
};

export default PipelineDetail;
