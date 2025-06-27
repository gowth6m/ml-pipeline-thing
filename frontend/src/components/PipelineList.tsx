import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Plus, Workflow, Calendar, Play, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Pipeline } from "@/types/pipeline";
import { api } from "@/lib/api";

interface PipelineListProps {
    onSelectPipeline: (pipeline: Pipeline) => void;
    onCreatePipeline: () => void;
}

export function PipelineList({
    onSelectPipeline,
    onCreatePipeline,
}: PipelineListProps) {
    const {
        data: pipelinesData,
        isLoading,
        error,
        refetch,
    } = useQuery({
        queryKey: ["pipelines"],
        queryFn: () => api.pipelines.list(),
        retry: 2,
        staleTime: 30000,
    });

    const pipelines = pipelinesData?.items || [];

    const formatDate = (dateStr: string) => {
        return new Date(dateStr).toLocaleDateString("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    };

    if (error) {
        return (
            <div className="space-y-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">
                            ML Pipeline Thing
                        </h1>
                        <p className="text-gray-600 mt-1">
                            Manage and monitor your machine learning workflows
                        </p>
                    </div>
                    <Button
                        onClick={onCreatePipeline}
                        className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        Create Pipeline
                    </Button>
                </div>

                <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                        Failed to load pipelines. {error.message}
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
                    <h1 className="text-3xl font-bold text-gray-900">
                        ML Pipeline Thing
                    </h1>
                    <p className="text-gray-600 mt-1">
                        Manage and monitor your machine learning workflows
                    </p>
                </div>
                <Button
                    onClick={onCreatePipeline}
                    className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                    disabled={isLoading}
                >
                    <Plus className="w-4 h-4 mr-2" />
                    Create Pipeline
                </Button>
            </div>

            {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3].map((i) => (
                        <Card key={i} className="animate-pulse">
                            <CardHeader>
                                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-2">
                                    <div className="h-3 bg-gray-200 rounded"></div>
                                    <div className="h-3 bg-gray-200 rounded w-5/6"></div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {pipelines.map((pipeline) => (
                        <Card
                            key={pipeline.id}
                            className="hover:shadow-lg transition-all duration-200 border-l-4 border-l-purple-500 bg-white/90 backdrop-blur-sm cursor-pointer"
                            onClick={() => onSelectPipeline(pipeline)}
                        >
                            <CardHeader className="pb-3">
                                <div className="flex items-start justify-between">
                                    <div className="flex items-center gap-2">
                                        <Workflow className="w-5 h-5 text-purple-600" />
                                        <CardTitle className="text-lg text-gray-900">
                                            {pipeline.name}
                                        </CardTitle>
                                    </div>
                                    <Badge
                                        variant="secondary"
                                        className={`bg-green-100 ${
                                            pipeline.status === "PENDING"
                                                ? "bg-yellow-100"
                                                : "bg-green-100"
                                        }`}
                                    >
                                        {pipeline.status}
                                    </Badge>
                                </div>
                                <CardDescription className="text-gray-600 line-clamp-2">
                                    {pipeline.description}
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="flex items-center gap-4 text-sm text-gray-500">
                                    <div className="flex items-center gap-1">
                                        <Calendar className="w-4 h-4" />
                                        <span>
                                            Updated{" "}
                                            {formatDate(pipeline.updatedAt)}
                                        </span>
                                    </div>
                                </div>
                                <div className="flex items-center justify-between pt-2 border-t border-gray-100">
                                    <span className="text-sm text-gray-500">
                                        Created {formatDate(pipeline.createdAt)}
                                    </span>
                                    <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            onSelectPipeline(pipeline);
                                        }}
                                    >
                                        <Play className="w-3 h-3 mr-1" />
                                        View
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                    {pipelines.length === 0 && (
                        <div className="col-span-full text-center py-12">
                            <Workflow className="w-16 h-16 mx-auto text-gray-300 mb-4" />
                            <h3 className="text-lg font-medium text-gray-900 mb-2">
                                No pipelines found
                            </h3>
                            <p className="text-gray-500 mb-4">
                                Get started by creating your first ML pipeline
                            </p>
                            <Button onClick={onCreatePipeline}>
                                <Plus className="w-4 h-4 mr-2" />
                                Create Pipeline
                            </Button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
