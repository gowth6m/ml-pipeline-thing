import { Workflow, Play, History, Plus, Home } from "lucide-react";
import { useLocation, useNavigate } from "react-router-dom";
import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarHeader,
} from "@/components/ui/sidebar";

export function AppSidebar() {
    const navigate = useNavigate();
    const location = useLocation();

    const mainItems = [
        {
            title: "Dashboard",
            icon: Home,
            path: "/pipelines",
        },
        {
            title: "Create Pipeline",
            icon: Plus,
            path: "/create-pipeline",
        },
    ];

    // Extract pipeline ID from URL if available
    const pipelineId = location.pathname.match(/\/pipeline\/([^\\/]+)/)?.[1];
    const pipeline = location.state?.pipeline;

    const pipelineItems =
        pipelineId && pipeline
            ? [
                  {
                      title: "Pipeline View",
                      icon: Workflow,
                      path: `/pipeline/${pipelineId}`,
                  },
                  {
                      title: "Run History",
                      icon: History,
                      path: `/pipeline/${pipelineId}/runs`,
                  },
              ]
            : [];

    return (
        <Sidebar className="border-r border-purple-200 bg-white/80 backdrop-blur-sm">
            <SidebarHeader className="p-6">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                        <Workflow className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h2 className="text-lg font-semibold text-gray-900">
                            ML Pipeline Thing
                        </h2>
                        <p className="text-xs text-gray-500">
                            by{" "}
                            <a
                                href="https://gowtham.io"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:text-blue-600"
                            >
                                @gowth6m
                            </a>
                        </p>
                    </div>
                </div>
            </SidebarHeader>
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel className="text-purple-700 font-medium">
                        Navigation
                    </SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {mainItems.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton
                                        onClick={() => navigate(item.path)}
                                        className={`${
                                            location.pathname === item.path
                                                ? "bg-purple-100 text-purple-700 border-l-4 border-purple-500"
                                                : "hover:bg-purple-50"
                                        }`}
                                    >
                                        <item.icon className="w-4 h-4" />
                                        <span>{item.title}</span>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>

                {pipelineItems.length > 0 && (
                    <SidebarGroup>
                        <SidebarGroupLabel className="text-blue-700 font-medium">
                            Pipeline: {pipeline?.name}
                        </SidebarGroupLabel>
                        <SidebarGroupContent>
                            <SidebarMenu>
                                {pipelineItems.map((item) => (
                                    <SidebarMenuItem key={item.title}>
                                        <SidebarMenuButton
                                            onClick={() =>
                                                navigate(item.path, {
                                                    state: { pipeline },
                                                })
                                            }
                                            className={`${
                                                location.pathname === item.path
                                                    ? "bg-blue-100 text-blue-700 border-l-4 border-blue-500"
                                                    : "hover:bg-blue-50"
                                            }`}
                                        >
                                            <item.icon className="w-4 h-4" />
                                            <span>{item.title}</span>
                                        </SidebarMenuButton>
                                    </SidebarMenuItem>
                                ))}
                            </SidebarMenu>
                        </SidebarGroupContent>
                    </SidebarGroup>
                )}
            </SidebarContent>
        </Sidebar>
    );
}
