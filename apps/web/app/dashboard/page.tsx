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
    } catch (err) {
      console.error("Failed to fetch jobs:", err)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("token")
    router.push("/")
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
                      <a
                        href={`/api/download/${job.id}`}
                        download
                        className="text-blue-600 hover:underline"
                      >
                        Download Results
                      </a>
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

