"use client";
import { ProductProps } from "@/lib/types";
import Link from "next/link";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { editData, fetchData } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";


export default function Home() {
  const queryClient = useQueryClient();

  const { data: products, isLoading: isLoadingProducts, isError: isErrorProducts } = useQuery({
    queryKey: ["products"],
    queryFn: fetchProducts
  });

  const deleteMutation = useMutation({
    mutationFn: (productId: string) => {
      return editData(`products/${productId}`, "DELETE");
    },
    onSuccess: () => {
      alert(`Produkt usunięty`);
      queryClient.invalidateQueries({ queryKey: ["products"] });
    },
    onError: () => {
      alert(`Nie udało się usunąć produktu`);
    }
  });

  if (isLoadingProducts || !products) {
    return (
      <div>loading...</div>

    );
  }
  if (isErrorProducts) {
    return <div>error</div>;
  }


  const handleDelete = (id: number) => {
    if (confirm("Czy na pewno chcesz usunąć ten produkt?")) {
      deleteMutation.mutate(id.toString());
    }
  };

  const handleAssign = (id: number) => {
    if (confirm("Czy na pewno chcesz przypisać ten produkt?")) {
      deleteMutation.mutate(id.toString());
    }
  };

  return (
    <div className={"flex flex-col justify-center items-center mt-4 space-y-6"}>
      {products.length === 0 ? (
        <p>Nie dodano żadnych produktów</p>
      ) : (
        products.map((item: ProductProps) => (
          <Card key={item.id} className="w-[600px]">
            <CardHeader>
              <CardTitle>{item.name}, {item.price} zł</CardTitle>
              <CardDescription>{item.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className={"flex flex-col justify-center align-items-center"}>
                <div className={"space-x-4 flex"}>
                  <div className={"flex justify-center items-center py-1 px-3 rounded bg-zinc-900 text-white max-w-24 text-sm"}>
                    <Link href={`/edit-product/${item.id}`}>Edytuj</Link>
                  </div>
                  <Button onClick={() => handleDelete(item.id)}>Usuń</Button>
                  <Button onClick={() => handleAssign(item.id)}>Przypisz</Button>
                </div>

              </div>
            </CardContent>
          </Card>
        ))
      )}
    </div>
  );
}

const fetchProducts = async () => fetchData<ProductProps[]>("products");