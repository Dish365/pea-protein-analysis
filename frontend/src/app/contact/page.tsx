"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import {
  ArrowRight,
  Mail,
  MessageSquare,
  Phone,
  Clock,
  Globe,
  HelpCircle
} from 'lucide-react';

const supportCategories = [
  { value: "technical", label: "Technical Support" },
  { value: "analysis", label: "Analysis Help" },
  { value: "account", label: "Account Issues" },
  { value: "feedback", label: "Feedback & Suggestions" },
  { value: "other", label: "Other" }
] as const;

const supportInfo = [
  {
    icon: Mail,
    title: "Email Support",
    description: "Get help via email within 24 hours",
    detail: "contact@proteinanalysis.io"
  },
  {
    icon: Phone,
    title: "Phone Support",
    description: "Available during business hours",
    detail: "+1 (xxx) xxx-xxxx"
  },
  {
    icon: Clock,
    title: "Available Hours",
    description: "When we're available",
    detail: "Mon-Fri: 9AM-6PM EST"
  },
  {
    icon: Globe,
    title: "Global Support",
    description: "Support in multiple languages",
    detail: "English, French"
  }
] as const;

export default function ContactPage() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageSquare className="h-6 w-6" />
              <h1 className="text-2xl font-bold">Contact Us</h1>
            </div>
            <Button asChild variant="outline" size="sm">
              <Link href="/dashboard" className="gap-2">
                Go to Dashboard
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto py-8 space-y-12">
        {/* Introduction */}
        <section className="max-w-4xl mx-auto text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight">
            Get in Touch
          </h1>
          <p className="text-lg text-muted-foreground">
            Have questions? We're here to help with any inquiries about our platform
          </p>
        </section>

        <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {/* Contact Form */}
          <Card className="md:row-span-2">
            <CardHeader>
              <CardTitle>Send us a Message</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="name">Name</Label>
                    <Input id="name" placeholder="Your name" required />
                  </div>
                  
                  <div className="grid gap-2">
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" placeholder="Your email" required />
                  </div>

                  <div className="grid gap-2">
                    <Label htmlFor="category">Category</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select a category" />
                      </SelectTrigger>
                      <SelectContent>
                        {supportCategories.map((category) => (
                          <SelectItem key={category.value} value={category.value}>
                            {category.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="grid gap-2">
                    <Label htmlFor="message">Message</Label>
                    <Textarea
                      id="message"
                      placeholder="How can we help?"
                      className="min-h-[150px]"
                      required
                    />
                  </div>
                </div>

                <Button type="submit" className="w-full">
                  Send Message
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Support Info */}
          <div className="space-y-6">
            {supportInfo.map((item) => (
              <Card key={item.title}>
                <CardContent className="pt-6">
                  <div className="flex items-start gap-4">
                    <div className="rounded-full p-2 bg-primary/10">
                      <item.icon className="h-4 w-4 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-medium">{item.title}</h3>
                      <p className="text-sm text-muted-foreground">
                        {item.description}
                      </p>
                      <p className="text-sm font-medium mt-1">
                        {item.detail}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* FAQ Link */}
          <Card className="bg-primary/5 border-primary/10">
            <CardContent className="pt-6">
              <div className="flex items-start gap-4">
                <div className="rounded-full p-2 bg-primary/10">
                  <HelpCircle className="h-4 w-4 text-primary" />
                </div>
                <div className="space-y-2">
                  <h3 className="font-medium">Need Quick Answers?</h3>
                  <p className="text-sm text-muted-foreground">
                    Check our documentation for immediate assistance with common questions
                  </p>
                  <Button variant="outline" asChild className="gap-2">
                    <Link href="/documentation">
                      View Documentation
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
} 