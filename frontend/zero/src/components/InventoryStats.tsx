import React from 'react';
import { CheckCircle, Clock, AlertTriangle, Package } from 'lucide-react';
import type { InventoryStats } from '../types';

interface InventoryStatsProps {
  stats: InventoryStats;
}

export function InventoryStats({ stats }: InventoryStatsProps) {
  const statCards = [
    {
      label: 'Total Items',
      value: stats.totalItems,
      icon: Package,
      color: 'text-blue-500',
      bgColor: 'bg-blue-50',
    },
    {
      label: 'Fresh Items',
      value: stats.freshItems,
      icon: CheckCircle,
      color: 'text-green-500',
      bgColor: 'bg-green-50',
    },
    {
      label: 'Expiring Soon',
      value: stats.expiringSoonItems,
      icon: Clock,
      color: 'text-yellow-500',
      bgColor: 'bg-yellow-50',
    },
    {
      label: 'Expired',
      value: stats.expiredItems,
      icon: AlertTriangle,
      color: 'text-red-500',
      bgColor: 'bg-red-50',
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {statCards.map((stat) => (
        <div
          key={stat.label}
          className={`${stat.bgColor} rounded-lg p-4 flex flex-col items-center justify-center`}
        >
          <stat.icon className={`w-8 h-8 ${stat.color} mb-2`} />
          <span className="text-2xl font-bold">{stat.value}</span>
          <span className="text-sm text-gray-600">{stat.label}</span>
        </div>
      ))}
    </div>
  );
}