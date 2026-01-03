"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import api from "@/lib/api"
import type { Job } from "@strava-saas/shared"

export default function DashboardPage() {
  const router = useRouter()
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [downloading, setDownloading] = useState<number | null>(null)

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) {
      router.push("/auth/login")
      return
    }

    fetchJobs()
  }, [router])

  const fetchJobs = async () => {
    try {
      const response = await api.get("/api/jobs/")
      setJobs(response.data)
    } catch (err: any) {
      console.error("Failed to fetch jobs:", err)
      if (err.response?.status === 401) {
        // Token expired, redirect to login
        localStorage.removeItem("token")
        router.push("/auth/login")
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("token")
    router.push("/")
  }

  const handleDownload = async (jobId: number) => {
    try {
      setDownloading(jobId)
      const token = localStorage.getItem("token")
      if (!token) {
        alert("Please login again")
        router.push("/auth/login")
        return
      }

      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
      const response = await fetch(`${API_URL}/api/download/${jobId}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem("token")
          router.push("/auth/login")
          return
        }
        const errorText = await response.text()
        throw new Error(errorText || "Download failed")
      }

      // Get the blob
      const blob = await response.blob()
      
      // Create download link
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `strava-visualizations-${jobId}.zip`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error: any) {
      console.error("Download error:", error)
      alert(error.message || "Failed to download file. Please try again.")
    } finally {
      setDownloading(null)
    }
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <div className="flex gap-4">
            <Link href="/upload">
              <Button>New Upload</Button>
            </Link>
            <Button variant="outline" onClick={handleLogout}>
              Logout
            </Button>
          </div>
        </div>

        <div className="grid gap-4">
          {jobs.length === 0 ? (
            <Card>
              <CardContent className="pt-6">
                <p className="text-center text-gray-500">
                  No jobs yet. <Link href="/upload" className="text-blue-600">Upload a file</Link> to get started.
                </p>
              </CardContent>
            </Card>
          ) : (
            jobs.map((job) => (
              <Card key={job.id}>
                <CardHeader>
                  <CardTitle>Job #{job.id}</CardTitle>
                  <CardDescription>
                    Status: <span className="font-semibold">{job.status}</span>
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="text-sm text-gray-600">
                        Created: {new Date(job.created_at).toLocaleString()}
                      </p>
                      {job.completed_at && (
                        <p className="text-sm text-gray-600">
                          Completed: {new Date(job.completed_at).toLocaleString()}
                        </p>
                      )}
                    </div>
                    {job.status === "completed" && (
                      <Button
                        onClick={() => handleDownload(job.id)}
                        variant="outline"
                        size="sm"
                        disabled={downloading === job.id}
                      >
                        {downloading === job.id ? "Downloading..." : "Download Results"}
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
