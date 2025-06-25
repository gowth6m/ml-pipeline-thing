import { useState, useCallback } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
    ReactFlow,
    Background,
    Controls,
    MiniMap,
    useNodesState,
    useEdgesState,
    Node,
    Edge,
    MarkerType,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { Play, Clock, CheckCircle, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Pipeline } from "@/types/pipeline";
import { api } from "@/lib/api";
import { toast } from "@/hooks/use-toast";

interface PipelineViewProps {
    pipeline: Pipeline;
    onViewRuns: () => void;
}

export function PipelineView({ pipeline, onViewRuns }: PipelineViewProps) {
    const queryClient = useQueryClient();

    const triggerRunMutation = useMutation({
        mutationFn: (request: {
            environment?: string;
            triggeredBy?: string;
            notes?: string;
        }) =>
            api.runs.trigger(pipeline.id, {
                environment: request.environment || "development",
                triggeredBy: request.triggeredBy || "manual",
                notes: request.notes,
            }),
        onSuccess: (data) => {
            queryClient.invalidateQueries({
                queryKey: ["pipeline-runs", pipeline.id],
            });
            toast({
                title: "Pipeline Run Started",
                description: `Pipeline run #${data.runId} has been triggered successfully.`,
            });
        },
        onError: (error) => {
            toast({
                title: "Failed to Start Pipeline",
                description: `Error: ${error.message}`,
                variant: "destructive",
            });
        },
    });

    // Convert pipeline steps to React Flow nodes
    const createNodesFromSteps = useCallback(() => {
        const nodes: Node[] = [];
        const positions: { [key: string]: { x: number; y: number } } = {};

        // Simple layout algorithm - arrange nodes in levels based on dependencies
        const levels: { [key: string]: number } = {};
        const nodeLevels: string[][] = [];

        // Calculate levels for each node
        const calculateLevel = (
            stepId: string,
            visited: Set<string> = new Set()
        ): number => {
            if (visited.has(stepId)) return 0; // Avoid circular dependencies
            visited.add(stepId);

            if (levels[stepId] !== undefined) return levels[stepId];

            const stage = pipeline.stages?.find((s) => s.id === stepId);
            if (
                !stage ||
                !stage.dependencies ||
                stage.dependencies.length === 0
            ) {
                levels[stepId] = 0;
                return 0;
            }

            const maxDepLevel = Math.max(
                ...stage.dependencies.map((dep) => calculateLevel(dep, visited))
            );
            levels[stepId] = maxDepLevel + 1;
            return levels[stepId];
        };

        // Calculate levels for all stages
        pipeline.stages?.forEach((stage) => calculateLevel(stage.id));

        // Group nodes by level
        pipeline.stages?.forEach((stage) => {
            const level = levels[stage.id];
            if (!nodeLevels[level]) nodeLevels[level] = [];
            nodeLevels[level].push(stage.id);
        });

        // Position nodes
        nodeLevels.forEach((levelNodes, level) => {
            levelNodes.forEach((nodeId, index) => {
                positions[nodeId] = {
                    x: level * 250,
                    y: index * 120 + (level % 2) * 60,
                };
            });
        });

        // Create nodes
        pipeline.stages?.forEach((stage) => {
            nodes.push({
                id: stage.id,
                type: "default",
                position: positions[stage.id],
                data: {
                    label: (
                        <div className="text-center p-2">
                            <div className="font-semibold text-sm">
                                {stage.name}
                            </div>
                            <div className="text-xs text-gray-300 mt-1">
                                {stage.stageType}
                            </div>
                        </div>
                    ),
                },
                style: {
                    background:
                        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    color: "white",
                    border: "2px solid #4c63d2",
                    borderRadius: "8px",
                    width: 200,
                    fontSize: "12px",
                },
            });
        });

        return nodes;
    }, [pipeline.stages]);

    // Convert dependencies to React Flow edges
    const createEdgesFromDependencies = useCallback(() => {
        const edges: Edge[] = [];

        pipeline.stages?.forEach((stage) => {
            stage.dependencies?.forEach((depId) => {
                edges.push({
                    id: `${depId}-${stage.id}`,
                    source: depId,
                    target: stage.id,
                    type: "smoothstep",
                    markerEnd: {
                        type: MarkerType.ArrowClosed,
                        color: "#4c63d2",
                    },
                    style: {
                        stroke: "#4c63d2",
                        strokeWidth: 2,
                    },
                });
            });
        });

        return edges;
    }, [pipeline.stages]);

    const [nodes] = useNodesState(createNodesFromSteps());
    const [edges] = useEdgesState(createEdgesFromDependencies());

    const handleTriggerRun = () => {
        triggerRunMutation.mutate({
            environment: "development",
            triggeredBy: "manual",
            notes: `Manual run triggered from UI for pipeline: ${pipeline.name}`,
        });
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">
                        {pipeline.name}
                    </h1>
                    <p className="text-gray-600 mt-1">{pipeline.description}</p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" onClick={onViewRuns}>
                        <Clock className="w-4 h-4 mr-2" />
                        View Runs
                    </Button>
                    <Button
                        onClick={handleTriggerRun}
                        disabled={triggerRunMutation.isPending}
                        className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700"
                    >
                        {triggerRunMutation.isPending ? (
                            <>
                                <AlertCircle className="w-4 h-4 mr-2 animate-spin" />
                                Triggering...
                            </>
                        ) : (
                            <>
                                <Play className="w-4 h-4 mr-2" />
                                Trigger Run
                            </>
                        )}
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <Card className="lg:col-span-2 bg-white/90 backdrop-blur-sm">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <CheckCircle className="w-5 h-5 text-green-600" />
                            Pipeline Flow
                        </CardTitle>
                        <CardDescription>
                            Interactive visualization of your pipeline steps and
                            dependencies
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="h-96 border border-gray-200 rounded-lg bg-gradient-to-br from-gray-50 to-blue-50">
                            <ReactFlow
                                nodes={nodes}
                                edges={edges}
                                fitView
                                fitViewOptions={{ padding: 0.2 }}
                                nodesDraggable={false}
                                nodesConnectable={false}
                                elementsSelectable={true}
                                proOptions={{
                                    hideAttribution: true,
                                }}
                            >
                                <Background color="#e5e7eb" gap={16} />
                            </ReactFlow>
                        </div>
                    </CardContent>
                </Card>

                <div className="space-y-4">
                    <Card className="bg-white/90 backdrop-blur-sm">
                        <CardHeader>
                            <CardTitle className="text-lg">
                                Pipeline Info
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3">
                            <div className="flex justify-between items-center">
                                <span className="text-gray-600">
                                    Total Stages:
                                </span>
                                <Badge variant="secondary">
                                    {pipeline.stages?.length || 0}
                                </Badge>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-gray-600">Created:</span>
                                <span className="text-sm">
                                    {new Date(
                                        pipeline.createdAt
                                    ).toLocaleDateString()}
                                </span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-gray-600">Updated:</span>
                                <span className="text-sm">
                                    {new Date(
                                        pipeline.updatedAt
                                    ).toLocaleDateString()}
                                </span>
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-white/90 backdrop-blur-sm">
                        <CardHeader>
                            <CardTitle className="text-lg">
                                Pipeline Stages
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-3">
                                {pipeline.stages?.map((stage, index) => (
                                    <div
                                        key={stage.id}
                                        className="p-3 border border-gray-200 rounded-lg bg-gray-50"
                                    >
                                        <div className="flex items-center gap-2 mb-2">
                                            <Badge
                                                variant="outline"
                                                className="text-xs"
                                            >
                                                {index + 1}
                                            </Badge>
                                            <span className="font-medium text-sm">
                                                {stage.name}
                                            </span>
                                        </div>
                                        <div className="text-xs text-gray-600 bg-gray-100 p-2 rounded">
                                            Type: {stage.stageType}
                                        </div>
                                        {stage.dependencies &&
                                            stage.dependencies.length > 0 && (
                                                <div className="mt-2 text-xs text-gray-500">
                                                    Dependencies:{" "}
                                                    {stage.dependencies.join(
                                                        ", "
                                                    )}
                                                </div>
                                            )}
                                    </div>
                                )) || (
                                    <div className="text-center py-4 text-gray-500">
                                        No stages defined for this pipeline
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
