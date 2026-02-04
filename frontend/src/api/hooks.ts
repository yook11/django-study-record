import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { client } from "./client";
import type { components } from "./schema";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const useGetItems = () => {
    return useQuery({
        queryKey: ["items"],
        queryFn: async () => {
            const { data, error } = await client.GET("/api/items");
            if (error) throw error;
            return data;
        }  
    })
}

export const useCreateItem = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (newItem: components["schemas"]["ItemCreateSchema"]) => {
            const { data, error } = await client.POST("/api/items", {body: newItem});
            if (error) throw error;
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["items"] });
        },
    }); 
}

export const useGetItem = (itemId: number) => {
    return useQuery({
        queryKey: ["items", itemId],
        queryFn: async () => {
            const { data, error } = await client.GET("/api/items/{item_id}", {
                params: { path: { item_id: itemId } }
            });
            if (error) throw error;
            return data;
        },
        enabled: !!itemId,
    });
};

export const useUpdateItem = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async ({ itemId, data }: {
            itemId: number;
            data: components["schemas"]["ItemCreateSchema"]
        }) => {
            const { data: result, error } = await client.PUT("/api/items/{item_id}", {
                params: { path: { item_id: itemId } },
                body: data,
            });
            if (error) throw error;
            return result;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["items"] });
        },
    });
};

export const useDeleteItem = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (itemId: number) => {
            const { error } = await client.DELETE("/api/items/{item_id}", {
                params: { path: { item_id: itemId } }
            });
            if (error) throw error;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["items"] });
        },
    });
};

export const useLogin = () => {
    const navigate = useNavigate();

    return useMutation({
        mutationFn: async (credentials: { username: string; password: string }) => {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(credentials),
            });

            if (!response.ok) {
                throw new Error('ログインに失敗しました');
            }

            return response.json();
        },
        onSuccess: () => {
            navigate('/items');
        },
    });
};


