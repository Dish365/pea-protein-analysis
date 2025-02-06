"use client";

import React, { useState } from "react";
import { Card, Form, Switch, Select, InputNumber, Button, message } from "antd";
import { SaveOutlined } from "@ant-design/icons";
import { useSettings } from "@/hooks/useSettings";

export default function SettingsPage() {
  const [loading, setLoading] = useState(false);
  const { settings, updateSettings } = useSettings();
  const [form] = Form.useForm();

  const handleUpdateSettings = async (values: any) => {
    try {
      setLoading(true);
      await updateSettings(values);
      message.success("Settings updated successfully");
    } catch (error: any) {
      message.error(error.message || "Failed to update settings");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-semibold mb-6">Application Settings</h1>

      <Form
        form={form}
        layout="vertical"
        initialValues={settings}
        onFinish={handleUpdateSettings}
      >
        <Card title="Analysis Settings" className="mb-6">
          <Form.Item
            label="Default Process Type"
            name="defaultProcessType"
            rules={[{ required: true }]}
          >
            <Select
              options={[
                { value: "baseline", label: "Baseline Process" },
                { value: "rf", label: "RF Process" },
                { value: "ir", label: "IR Process" },
              ]}
            />
          </Form.Item>

          <Form.Item
            label="Analysis Cache Duration (minutes)"
            name="cacheDuration"
            rules={[{ required: true }]}
          >
            <InputNumber min={1} max={60} />
          </Form.Item>

          <Form.Item
            label="Auto-refresh Results"
            name="autoRefresh"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            label="Refresh Interval (seconds)"
            name="refreshInterval"
            rules={[{ required: true }]}
          >
            <InputNumber min={5} max={60} />
          </Form.Item>
        </Card>

        <Card title="Display Settings" className="mb-6">
          <Form.Item
            label="Theme"
            name="theme"
            rules={[{ required: true }]}
          >
            <Select
              options={[
                { value: "light", label: "Light" },
                { value: "dark", label: "Dark" },
                { value: "system", label: "System" },
              ]}
            />
          </Form.Item>

          <Form.Item
            label="Default Chart Type"
            name="defaultChartType"
            rules={[{ required: true }]}
          >
            <Select
              options={[
                { value: "bar", label: "Bar Chart" },
                { value: "line", label: "Line Chart" },
                { value: "pie", label: "Pie Chart" },
              ]}
            />
          </Form.Item>

          <Form.Item
            label="Show Tooltips"
            name="showTooltips"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>
        </Card>

        <Card title="Notification Settings" className="mb-6">
          <Form.Item
            label="Email Notifications"
            name="emailNotifications"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            label="Analysis Completion Alerts"
            name="completionAlerts"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            label="Error Notifications"
            name="errorNotifications"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>
        </Card>

        <div className="flex justify-end">
          <Button
            type="primary"
            icon={<SaveOutlined />}
            loading={loading}
            htmlType="submit"
          >
            Save Settings
          </Button>
        </div>
      </Form>
    </div>
  );
} 