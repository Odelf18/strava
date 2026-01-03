"use client"

import { useEffect, useState } from "react"
import { useRouter, useParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import api from "@/lib/api"

type VisualizationType = "facets" | "map" | "elevations" | "landscape" | "calendar" | "dumbbell"
type PackType = "single" | "all" | "premium"

export default function ConfigurePage() {
  const router = useRouter()
  const params = useParams()
  const jobId = parseInt(params.jobId as string)

  const [selectedViz, setSelectedViz] = useState<VisualizationType>("facets")
  const [packType, setPackType] = useState<PackType>("single")
  const [hasFilters, setHasFilters] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  // Filter options
  const [sportTypes, setSportTypes] = useState<string[]>([])
  const [dateFrom, setDateFrom] = useState("")
  const [dateTo, setDateTo] = useState("")
  const [bbox, setBbox] = useState({ lon_min: "", lon_max: "", lat_min: "", lat_max: "" })
  const [activityIds, setActivityIds] = useState("")

  const visualizations: VisualizationType[] = [
    "facets",
    "map",
    "elevations",
    "landscape",
    "calendar",
    "dumbbell",
  ]

  const handleProceedToPayment = async () => {
    setLoading(true)
    setError("")

    try {
      // Determine which visualizations to include
      let visualizations: VisualizationType[] = []
      if (packType === "all") {
        visualizations = ["facets", "map", "elevations", "landscape", "calendar", "dumbbell"]
      } else if (packType === "premium") {
        visualizations = ["facets", "map", "elevations", "landscape", "calendar", "dumbbell"]
      } else {
        visualizations = [selectedViz]
      }

      // Build filters object
      const filters: any = {}
      if (hasFilters) {
        if (sportTypes.length > 0) filters.sport_types = sportTypes
        if (dateFrom) filters.date_from = dateFrom
        if (dateTo) filters.date_to = dateTo
        if (bbox.lon_min && bbox.lon_max && bbox.lat_min && bbox.lat_max) {
          filters.bbox = {
            lon_min: parseFloat(bbox.lon_min),
            lon_max: parseFloat(bbox.lon_max),
            lat_min: parseFloat(bbox.lat_min),
            lat_max: parseFloat(bbox.lat_max),
          }
        }
        if (activityIds) {
          filters.activity_ids = activityIds
            .split(",")
            .map((id) => parseInt(id.trim()))
            .filter((id) => !isNaN(id))
        }
      }

      // TEST MODE: Direct processing without payment
      await api.post(`/api/jobs/${jobId}/configure`, {
        job_id: jobId,
        pack_type: packType,
        visualization_type: packType === "single" ? selectedViz : undefined,
        visualizations,
        has_filters: hasFilters && Object.keys(filters).length > 0,
        filters: hasFilters && Object.keys(filters).length > 0 ? filters : undefined,
        success_url: `${window.location.origin}/dashboard`,
        cancel_url: `${window.location.origin}/configure/${jobId}`,
      })

      // Redirect to dashboard to see processing status
      router.push("/dashboard")
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to create payment session")
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <Card>
          <CardHeader>
            <CardTitle>Configure Your Visualizations</CardTitle>
            <CardDescription>Job #{jobId} - Choose your options and proceed to payment</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">{error}</div>
            )}

            {/* Pack Selection */}
            <div>
              <label className="block text-sm font-medium mb-2">Package Type</label>
              <div className="grid grid-cols-3 gap-4">
                <Card
                  className={`cursor-pointer ${packType === "single" ? "border-blue-500" : ""}`}
                  onClick={() => setPackType("single")}
                >
                  <CardContent className="pt-4">
                    <h3 className="font-semibold">Single</h3>
                    <p className="text-sm text-gray-600">$2.00</p>
                    <p className="text-xs text-gray-500 mt-1">One visualization</p>
                  </CardContent>
                </Card>
                <Card
                  className={`cursor-pointer ${packType === "all" ? "border-blue-500" : ""}`}
                  onClick={() => setPackType("all")}
                >
                  <CardContent className="pt-4">
                    <h3 className="font-semibold">All Pack</h3>
                    <p className="text-sm text-gray-600">$9.90</p>
                    <p className="text-xs text-gray-500 mt-1">All visualizations</p>
                  </CardContent>
                </Card>
                <Card
                  className={`cursor-pointer ${packType === "premium" ? "border-blue-500" : ""}`}
                  onClick={() => setPackType("premium")}
                >
                  <CardContent className="pt-4">
                    <h3 className="font-semibold">Premium</h3>
                    <p className="text-sm text-gray-600">$19.90</p>
                    <p className="text-xs text-gray-500 mt-1">5 generations with filters</p>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Visualization Selection (only for single pack) */}
            {packType === "single" && (
              <div>
                <label className="block text-sm font-medium mb-2">Visualization Type</label>
                <div className="grid grid-cols-3 gap-2">
                  {visualizations.map((viz) => (
                    <button
                      key={viz}
                      type="button"
                      onClick={() => setSelectedViz(viz)}
                      className={`px-4 py-2 rounded border ${
                        selectedViz === viz
                          ? "bg-blue-500 text-white border-blue-500"
                          : "bg-white border-gray-300"
                      }`}
                    >
                      {viz.charAt(0).toUpperCase() + viz.slice(1)}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Filters Toggle */}
            <div>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={hasFilters}
                  onChange={(e) => setHasFilters(e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm font-medium">
                  Apply Filters {packType === "single" && hasFilters && " (+$1.00)"}
                </span>
              </label>
            </div>

            {/* Filter Options */}
            {hasFilters && (
              <div className="space-y-4 p-4 bg-gray-50 rounded-md">
                <div>
                  <label className="block text-sm font-medium mb-1">Sport Types (comma-separated)</label>
                  <input
                    type="text"
                    value={sportTypes.join(", ")}
                    onChange={(e) =>
                      setSportTypes(
                        e.target.value.split(",").map((s) => s.trim()).filter((s) => s)
                      )
                    }
                    placeholder="e.g., Vélo, Running, Swimming"
                    className="w-full px-3 py-2 border rounded-md"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Date From</label>
                    <input
                      type="date"
                      value={dateFrom}
                      onChange={(e) => setDateFrom(e.target.value)}
                      className="w-full px-3 py-2 border rounded-md"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Date To</label>
                    <input
                      type="date"
                      value={dateTo}
                      onChange={(e) => setDateTo(e.target.value)}
                      className="w-full px-3 py-2 border rounded-md"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">
                    Geographic Bounds (Bounding Box)
                  </label>
                  <div className="grid grid-cols-4 gap-2">
                    <input
                      type="number"
                      step="any"
                      value={bbox.lon_min}
                      onChange={(e) => setBbox({ ...bbox, lon_min: e.target.value })}
                      placeholder="Lon Min"
                      className="px-3 py-2 border rounded-md"
                    />
                    <input
                      type="number"
                      step="any"
                      value={bbox.lon_max}
                      onChange={(e) => setBbox({ ...bbox, lon_max: e.target.value })}
                      placeholder="Lon Max"
                      className="px-3 py-2 border rounded-md"
                    />
                    <input
                      type="number"
                      step="any"
                      value={bbox.lat_min}
                      onChange={(e) => setBbox({ ...bbox, lat_min: e.target.value })}
                      placeholder="Lat Min"
                      className="px-3 py-2 border rounded-md"
                    />
                    <input
                      type="number"
                      step="any"
                      value={bbox.lat_max}
                      onChange={(e) => setBbox({ ...bbox, lat_max: e.target.value })}
                      placeholder="Lat Max"
                      className="px-3 py-2 border rounded-md"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">
                    Activity IDs (comma-separated)
                  </label>
                  <input
                    type="text"
                    value={activityIds}
                    onChange={(e) => setActivityIds(e.target.value)}
                    placeholder="e.g., 123, 456, 789"
                    className="w-full px-3 py-2 border rounded-md"
                  />
                </div>
              </div>
            )}

            {/* Price Summary - Hidden in test mode */}
            <div className="p-4 bg-yellow-50 rounded-md border border-yellow-200">
              <div className="flex items-center gap-2">
                <span className="text-yellow-800 font-semibold">⚠️ TEST MODE</span>
                <span className="text-sm text-yellow-700">
                  Payment disabled - Processing will start immediately
                </span>
              </div>
              <div className="mt-2 text-xs text-yellow-600">
                Price would be:{" "}
                {packType === "premium"
                  ? "$19.90"
                  : packType === "all"
                    ? "$9.90"
                    : hasFilters
                      ? "$3.00"
                      : "$2.00"}
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-4">
              <Button
                onClick={handleProceedToPayment}
                disabled={loading}
                className="flex-1"
                size="lg"
              >
                {loading ? "Starting..." : "Start Processing (TEST MODE)"}
              </Button>
              <Button
                variant="outline"
                onClick={() => router.push("/dashboard")}
                disabled={loading}
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

