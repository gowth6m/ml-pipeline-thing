import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { DashboardLayout } from "@/components/DashboardLayout";
import Index from "./pages/Index";
import Pipelines from "./pages/Pipelines";
import PipelineDetail from "./pages/PipelineDetail";
import PipelineRuns from "./pages/PipelineRuns";
import CreatePipeline from "./pages/CreatePipeline";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
    <QueryClientProvider client={queryClient}>
        <TooltipProvider>
            <Toaster />
            <Sonner />
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Index />} />
                    <Route
                        path="/*"
                        element={
                            <DashboardLayout>
                                <Routes>
                                    <Route
                                        path="/pipelines"
                                        element={<Pipelines />}
                                    />
                                    <Route
                                        path="/pipeline/:pipelineId"
                                        element={<PipelineDetail />}
                                    />
                                    <Route
                                        path="/pipeline/:pipelineId/runs"
                                        element={<PipelineRuns />}
                                    />
                                    <Route
                                        path="/create-pipeline"
                                        element={<CreatePipeline />}
                                    />
                                    <Route path="*" element={<NotFound />} />
                                </Routes>
                            </DashboardLayout>
                        }
                    />
                </Routes>
            </BrowserRouter>
        </TooltipProvider>
    </QueryClientProvider>
);

export default App;
