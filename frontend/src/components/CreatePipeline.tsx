import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Trash2, Save, X, Pencil } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Pipeline } from "@/types/pipeline";
import { PipelineStageCreate, StageType } from "@/types";
import { api } from "@/lib/api";
import { toast } from "@/hooks/use-toast";

interface CreatePipelineProps {
    onPipelineCreated: (pipeline: Pipeline) => void;
    onCancel: () => void;
}

export function CreatePipeline({
    onPipelineCreated,
    onCancel,
}: CreatePipelineProps) {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [stages, setStages] = useState<PipelineStageCreate[]>([]);
    const [newStage, setNewStage] = useState({
        name: "",
        stageType: "" as StageType | "",
        customName: "",
        order: 0,
        dependencies: [] as string[],
    });

    const queryClient = useQueryClient();

    const createPipelineMutation = useMutation({
        mutationFn: api.pipelines.create,
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ["pipelines"] });
            toast({
                title: "Pipeline Created",
                description: `Pipeline "${data.name}" has been created successfully.`,
            });
            onPipelineCreated(data as Pipeline);
        },
        onError: (error) => {
            toast({
                title: "Error",
                description: `Failed to create pipeline: ${error.message}`,
                variant: "destructive",
            });
        },
    });

    const addStage = () => {
        if (!newStage.name.trim() || !newStage.stageType) {
            toast({
                title: "Invalid Stage",
                description: "Please provide both stage name and type.",
                variant: "destructive",
            });
            return;
        }

        // Validate custom name for CUSTOM stage type
        if (
            newStage.stageType === StageType.CUSTOM &&
            !newStage.customName.trim()
        ) {
            toast({
                title: "Invalid Stage",
                description:
                    "Please provide a custom name for custom stage type.",
                variant: "destructive",
            });
            return;
        }

        const stage: PipelineStageCreate = {
            name: newStage.name.trim(),
            stageType: newStage.stageType,
            customName:
                newStage.stageType === StageType.CUSTOM
                    ? newStage.customName.trim()
                    : undefined,
            order: stages.length,
            dependencies: newStage.dependencies,
        };

        setStages([...stages, stage]);
        setNewStage({
            name: "",
            stageType: "",
            customName: "",
            order: 0,
            dependencies: [],
        });

        toast({
            title: "Stage Added",
            description: `Stage "${stage.name}" has been added to the pipeline.`,
        });
    };

    const removeStage = (stageName: string) => {
        setStages(stages.filter((stage) => stage.name !== stageName));
        // Remove this stage from other stages' dependencies
        setStages((prevStages) =>
            prevStages.map((stage) => ({
                ...stage,
                dependencies:
                    stage.dependencies?.filter((dep) => dep !== stageName) ||
                    [],
            }))
        );
    };

    const toggleDependency = (stageName: string, dependencyName: string) => {
        setStages(
            stages.map((stage) => {
                if (stage.name === stageName) {
                    const currentDeps = stage.dependencies || [];
                    const newDependencies = currentDeps.includes(dependencyName)
                        ? currentDeps.filter((dep) => dep !== dependencyName)
                        : [...currentDeps, dependencyName];
                    return { ...stage, dependencies: newDependencies };
                }
                return stage;
            })
        );
    };

    const createPipeline = () => {
        if (!name.trim()) {
            toast({
                title: "Invalid Pipeline",
                description: "Please provide a pipeline name.",
                variant: "destructive",
            });
            return;
        }

        if (stages.length === 0) {
            toast({
                title: "Invalid Pipeline",
                description: "Please add at least one stage to the pipeline.",
                variant: "destructive",
            });
            return;
        }

        const pipelineData = {
            name: name.trim(),
            description: description.trim() || null,
            stages: stages,
        };

        createPipelineMutation.mutate(pipelineData);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">
                        Create New Pipeline
                    </h1>
                    <p className="text-gray-600 mt-1">
                        Define your ML pipeline steps and dependencies
                    </p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" onClick={onCancel}>
                        <X className="w-4 h-4 mr-2" />
                        Cancel
                    </Button>
                    <Button
                        onClick={createPipeline}
                        className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                        disabled={createPipelineMutation.isPending}
                    >
                        <Save className="w-4 h-4 mr-2" />
                        {createPipelineMutation.isPending
                            ? "Creating..."
                            : "Create Pipeline"}
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-6">
                    <Card className="bg-white/90 backdrop-blur-sm">
                        <CardHeader>
                            <CardTitle>Pipeline Details</CardTitle>
                            <CardDescription>
                                Basic information about your pipeline
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div>
                                <Label htmlFor="name">Pipeline Name</Label>
                                <Input
                                    id="name"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    placeholder="e.g., ML Training Pipeline"
                                    className="mt-1"
                                />
                            </div>
                            <div>
                                <Label htmlFor="description">Description</Label>
                                <Textarea
                                    id="description"
                                    value={description}
                                    onChange={(e) =>
                                        setDescription(e.target.value)
                                    }
                                    placeholder="Describe what this pipeline does..."
                                    className="mt-1"
                                    rows={3}
                                />
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-white/90 backdrop-blur-sm">
                        <CardHeader>
                            <CardTitle>Add New Stage</CardTitle>
                            <CardDescription>
                                Define a new stage for your pipeline
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div>
                                <Label htmlFor="stageName">Stage Name</Label>
                                <Input
                                    id="stageName"
                                    value={newStage.name}
                                    onChange={(e) =>
                                        setNewStage({
                                            ...newStage,
                                            name: e.target.value,
                                        })
                                    }
                                    placeholder="e.g., Data Preparation"
                                    className="mt-1"
                                />
                            </div>
                            <div>
                                <Label htmlFor="stageType">Stage Type</Label>
                                <Select
                                    value={newStage.stageType}
                                    onValueChange={(value: StageType) =>
                                        setNewStage({
                                            ...newStage,
                                            stageType: value,
                                            customName: "",
                                        })
                                    }
                                >
                                    <SelectTrigger className="mt-1">
                                        <SelectValue placeholder="Select a stage type" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value={StageType.CUSTOM}>
                                            <div className="flex flex-row items-center gap-2">
                                                Custom{" "}
                                                <Pencil className="w-4 h-4" />
                                            </div>
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.DATA_INGESTION}
                                        >
                                            Data Ingestion
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.DATA_VALIDATION}
                                        >
                                            Data Validation
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.DATA_PREPROCESSING}
                                        >
                                            Data Preprocessing
                                        </SelectItem>
                                        <SelectItem
                                            value={
                                                StageType.FEATURE_ENGINEERING
                                            }
                                        >
                                            Feature Engineering
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.DATA_SPLITTING}
                                        >
                                            Data Splitting
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.MODEL_TRAINING}
                                        >
                                            Model Training
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.MODEL_VALIDATION}
                                        >
                                            Model Validation
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.MODEL_EVALUATION}
                                        >
                                            Model Evaluation
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.MODEL_TESTING}
                                        >
                                            Model Testing
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.MODEL_REGISTRATION}
                                        >
                                            Model Registration
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.MODEL_DEPLOYMENT}
                                        >
                                            Model Deployment
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.MODEL_MONITORING}
                                        >
                                            Model Monitoring
                                        </SelectItem>
                                        <SelectItem
                                            value={
                                                StageType.EXPLORATORY_DATA_ANALYSIS
                                            }
                                        >
                                            Exploratory Data Analysis
                                        </SelectItem>
                                        <SelectItem
                                            value={
                                                StageType.HYPERPARAMETER_TUNING
                                            }
                                        >
                                            Hyperparameter Tuning
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.MODEL_COMPARISON}
                                        >
                                            Model Comparison
                                        </SelectItem>
                                        <SelectItem
                                            value={StageType.ENVIRONMENT_SETUP}
                                        >
                                            Environment Setup
                                        </SelectItem>
                                        <SelectItem
                                            value={
                                                StageType.RESOURCE_PROVISIONING
                                            }
                                        >
                                            Resource Provisioning
                                        </SelectItem>
                                        <SelectItem value={StageType.CLEANUP}>
                                            Cleanup
                                        </SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            {newStage.stageType === StageType.CUSTOM && (
                                <div>
                                    <Label htmlFor="customName">
                                        Custom Stage Name
                                    </Label>
                                    <Input
                                        id="customName"
                                        value={newStage.customName}
                                        onChange={(e) =>
                                            setNewStage({
                                                ...newStage,
                                                customName: e.target.value,
                                            })
                                        }
                                        placeholder="Enter custom stage name"
                                        className="mt-1"
                                    />
                                </div>
                            )}
                            <Button onClick={addStage} className="w-full">
                                <Plus className="w-4 h-4 mr-2" />
                                Add Stage
                            </Button>
                        </CardContent>
                    </Card>
                </div>

                <Card className="bg-white/90 backdrop-blur-sm">
                    <CardHeader>
                        <CardTitle>Pipeline Stages ({stages.length})</CardTitle>
                        <CardDescription>
                            Manage your pipeline stages and their dependencies
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        {stages.length === 0 ? (
                            <div className="text-center py-8 text-gray-500">
                                <Plus className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                                <p>
                                    No stages added yet. Add your first stage to
                                    get started.
                                </p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {stages.map((stage, index) => (
                                    <div
                                        key={stage.name}
                                        className="border border-gray-200 rounded-lg p-4 bg-gray-50"
                                    >
                                        <div className="flex items-start justify-between mb-3">
                                            <div className="flex items-center gap-2">
                                                <Badge
                                                    variant="outline"
                                                    className="text-xs"
                                                >
                                                    {index + 1}
                                                </Badge>
                                                <h4 className="font-medium">
                                                    {stage.name}
                                                </h4>
                                            </div>
                                            <Button
                                                size="sm"
                                                variant="outline"
                                                onClick={() =>
                                                    removeStage(stage.name)
                                                }
                                                className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                            >
                                                <Trash2 className="w-3 h-3" />
                                            </Button>
                                        </div>

                                        <div className="text-xs text-gray-600 bg-white p-2 rounded mb-3">
                                            <span className="font-medium">
                                                Type:{" "}
                                            </span>
                                            {stage.stageType}
                                            {stage.customName && (
                                                <>
                                                    <br />
                                                    <span className="font-medium">
                                                        Custom Name:{" "}
                                                    </span>
                                                    {stage.customName}
                                                </>
                                            )}
                                        </div>

                                        <div>
                                            <Label className="text-xs text-gray-500">
                                                Dependencies:
                                            </Label>
                                            <div className="flex flex-wrap gap-2 mt-1">
                                                {stages
                                                    .filter(
                                                        (s) =>
                                                            s.name !==
                                                            stage.name
                                                    )
                                                    .map((otherStage) => (
                                                        <Badge
                                                            key={
                                                                otherStage.name
                                                            }
                                                            variant={
                                                                (
                                                                    stage.dependencies ||
                                                                    []
                                                                ).includes(
                                                                    otherStage.name
                                                                )
                                                                    ? "default"
                                                                    : "outline"
                                                            }
                                                            className="cursor-pointer text-xs"
                                                            onClick={() =>
                                                                toggleDependency(
                                                                    stage.name,
                                                                    otherStage.name
                                                                )
                                                            }
                                                        >
                                                            {otherStage.name}
                                                        </Badge>
                                                    ))}
                                                {stages.filter(
                                                    (s) => s.name !== stage.name
                                                ).length === 0 && (
                                                    <span className="text-xs text-gray-400">
                                                        No other stages
                                                        available
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
