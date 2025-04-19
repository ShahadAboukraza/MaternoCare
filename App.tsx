import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AuthProvider } from "@/hooks/use-auth";
import { ProtectedRoute } from "@/lib/protected-route";
import NotFound from "@/pages/not-found";
import Layout from "@/components/Layout";
import Home from "@/pages/Home";
import WhatIsPCB from "@/pages/WhatIsPCB";
import Tips from "@/pages/Tips";
import PCBDiagram from "@/pages/PCBDiagram";
import Viewer from "@/pages/Viewer";
import Calculator from "@/pages/Calculator";
import DataUpload from "@/pages/DataUpload";
import AuthPage from "@/pages/AuthPage";
import ProfilePage from "@/pages/ProfilePage";
import React from "react";

function Router() {
  return (
    <Layout>
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/whatispcb" component={WhatIsPCB} />
        <Route path="/tips" component={Tips} />
        <Route path="/pcbdrawing" component={PCBDiagram} />
        <Route path="/viewer" component={Viewer} />
        <Route path="/calculator" component={Calculator} />
        <ProtectedRoute path="/data-upload" component={DataUpload} />
        <Route path="/auth" component={AuthPage} />
        <ProtectedRoute path="/profile" component={ProfilePage} />
        {/* Fallback to 404 */}
        <Route component={NotFound} />
      </Switch>
    </Layout>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
