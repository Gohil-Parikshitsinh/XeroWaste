export interface InventoryItem {
  id: string;
  name: string;
  quantity: number;
  expiryDate?: string;
  status: 'fresh' | 'expiring-soon' | 'expired';
}

export interface InventoryStats {
  totalItems: number;
  freshItems: number;
  expiringSoonItems: number;
  expiredItems: number;
}

export interface DetectionResult {
  items: InventoryItem[];
  timestamp: string;
  stats: InventoryStats;
}