import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { client } from "./client";
import type { components } from "./schema";

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


