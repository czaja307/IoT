"use client";
import { useParams } from "next/navigation";
import { ProductForm } from "@/components/ProductForm";
import Link from "next/link";
import { ArrowLeftIcon } from "@radix-ui/react-icons";

export default function EditProductPage(){
    const productId = useParams().productId;
    console.log(productId);

    return (
        <div>
            <div
                className={'flex border-2 border-gray-200 w-8 h-8 items-center justify-center rounded-lg m-4 hover:bg-gray-100'}>
                <Link href={'/'}>
                    <ArrowLeftIcon/>
                </Link>
            </div>
            {productId ? <ProductForm productId={Number(productId)}/> : <div>Error</div>}

        </div>
    )
}